#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#
from typing import Dict

from pinecone.protos import core_pb2
from pinecone.utils.constants import ZMQ_CONTROL_PORT, GATEWAY_NAME, OUT_POOL_SIZE
from pinecone.utils import get_hostname, replica_kube_hostname, replica_name
from pinecone.network.zmq.spec import ServletSpec, SocketType, Socket
from loguru import logger

import asyncio
import zmq
import zmq.asyncio
from collections import defaultdict
import os
import random

RECV_TIMEOUT = 0.5
SEND_TIMEOUT = 0.5


class ZMQServlet:

    def __init__(self, servlet_spec: ServletSpec):
        self.spec = servlet_spec

        self.wal = None
        self.poller = zmq.asyncio.Poller()
        self.exception = None
        self.log_in = None
        if len(self.spec.in_sockets) > 0:
            self.zmq_ins = [self.init_socket(in_sock)
                            for in_sock in self.spec.in_sockets]
            for zmq_sock in self.zmq_ins:
                self.poller.register(zmq_sock, zmq.POLLIN)

        self.control_sock = self.context.socket(zmq.PUSH)
        control_host = 'localhost' if self.spec.native else 'controller.default'
        self.control_sock.connect(
            'tcp://{}:{}'.format(control_host, ZMQ_CONTROL_PORT))

        if self.spec.log_in_socket is not None:
            self.log_in = self.init_socket(self.spec.log_in_socket)
            self.poller.register(self.log_in, zmq.POLLIN)

        if self.spec.log_out_sockets:
            self.log_outs = [self.init_socket(log_out_socket) for log_out_socket in self.spec.log_out_sockets]
        else:
            self.log_outs = []

        self._bind_outs = dict()
        self._zmq_out_pool = [self.zmq_out_socks for _ in range(0, OUT_POOL_SIZE)]

        self.msg_sent = 0
        self.msg_recv = 0
        self.total_msg = defaultdict(int)
        self.avg_time = defaultdict(int)
        self.gateway_outs = []
        self.in_buffer = asyncio.Queue()
        self.in_msgs = asyncio.Queue()
        self.heartbeat_msg = self.create_heartbeat_msg()

    def get_bind_out(self, s: Socket) -> zmq.Socket:
        assert s.bind
        if s.port not in self._bind_outs:
            self._bind_outs[s.port] = self.init_socket(s)
        return self._bind_outs[s.port]

    @property
    def zmq_out_socks(self):
        return {r: [self.get_bind_out(s) if s.bind else self.init_socket(s) for s in sockets]
                for r, sockets in self.spec.out_sockets.items()}

    @property
    def zmq_out(self) -> Dict[str, zmq.Socket]:
        if (self.msg_sent+1) % 100 == 0:
            old_socks = self._zmq_out_pool.pop(0)
            # for r, socks in old_socks.items():
            #     for sock in socks:
            #         sock.close()
            self._zmq_out_pool.append(self.zmq_out_socks)
        zmq_out = self._zmq_out_pool[random.randint(0, OUT_POOL_SIZE-1)]
        return zmq_out

    @property
    def context(self):
        return zmq.asyncio.Context()

    async def heartbeat(self):
        while True:
            status = core_pb2.Status(msg_recv=self.msg_recv,
                                     msg_sent=self.msg_sent,
                                     avg_time=self.avg_time,
                                     code=core_pb2.Status.StatusCode.READY,
                                     size=self.spec.get_stats().get('size', None))
            self.heartbeat_msg.status.CopyFrom(status)
            self.control_sock.send(self.heartbeat_msg.SerializeToString())
            if self.wal and not self.wal.leader:
                await self.send_log_msg(self.wal.get_replay_request(), 0)
            await asyncio.sleep(1)

    def create_heartbeat_msg(self) -> core_pb2.ServiceControlRequest:
        hostname = os.environ.get("HOSTNAME")
        return core_pb2.ServiceControlRequest(service=self.spec.service_name,
                                              function=self.spec.function_name if (hostname and 'deployment' in hostname) else hostname)

    async def handle_msg(self, msg: core_pb2.Request):
        route = core_pb2.Request.Route(function=os.environ.get("HOSTNAME"), function_id=self.spec.shard)
        route.start_time.GetCurrentTime()

        if self.spec.handle_msg:
            response = await self.spec.handle_msg(msg)
            route.end_time.GetCurrentTime()

            self.total_msg[msg.path] = self.total_msg[msg.path] + 1
            msg.routes.append(route)
            if response:
                if self.spec.shard != 0:
                    response.shard_num = self.spec.shard
                await self.send_msg(response)

    async def consume_msgs(self):
        while True:
            msg = await self.in_msgs.get()
            if msg.path == 'read' or self.wal.is_next(msg.client_id, msg.client_offset):
                await self.handle_msg(msg)
                while True:
                    try:
                        await self.in_msgs.put(self.in_buffer.get_nowait())
                    except asyncio.QueueEmpty:
                        break
            else:
                if msg.client_offset > self.wal.get_client_offset(msg.client_id):
                    await self.in_buffer.put(msg)
                elif msg.client_offset == self.wal.get_client_offset(msg.client_id):
                    await self.send_msg(msg)

    async def poll(self):
        while True:
            socks = dict(await self.poller.poll(timeout=2000))

            for sock_num, in_sock in enumerate(self.zmq_ins):
                if in_sock in socks:
                    msg = await self.recv_msg(sock_num)
                    if self.wal:
                        await self.in_msgs.put(msg)
                    else:
                        await self.handle_msg(msg)

                if self.log_in in socks:
                    msg = await self.recv_log_msg()
                    if self.spec.handle_log_msg:
                        await self.spec.handle_log_msg(msg)
                    else:
                        logger.warning("no log_msg handler defined")

    def get_gateway_sock(self, gateway_num: int, sock: Socket) -> zmq.Socket:
        while gateway_num >= len(self.gateway_outs):
            new_sock = Socket(sock.bind, sock_type=sock.sock_type, port=sock.port,
                              host=replica_name(sock.host, 0, len(self.gateway_outs)) if self.spec.native
                              else replica_kube_hostname(sock.host, 0, len(self.gateway_outs)))
            self.gateway_outs.append(self.init_socket(new_sock))
        return self.gateway_outs[gateway_num]

    async def send_msg(self, msg: 'core_pb2.Request'):
        self.msg_sent += 1
        send_sockets = []

        for path in {msg.path, '*'}:
            for sock in (sock for sock in self.spec.out_sockets.get(path, []) if sock.host == GATEWAY_NAME):
                send_sockets.append(self.get_gateway_sock(msg.gateway_num, sock))
                break
            else:
                send_sockets.extend(self.zmq_out.get(path, []))
                # logger.error(f"{os.environ.get('HOSTNAME')}: send socks: {[sock.host for sock in self.spec.out_sockets.get(path, [])]}")

        if len(send_sockets) == 0:
            logger.warning('{}: no out socket for path {}'.format(get_hostname(), msg.path))

        shard_msgs = self.spec.out_socket_selector.select_socket(msg, len(send_sockets))
        for socket, shard_msg in zip(send_sockets, shard_msgs):
            if shard_msg is not None:
                await socket.send(shard_msg.SerializeToString())

    async def send_log_msg(self, msg: 'core_pb2.LogEntry', replica: int):
        assert replica != self.spec.replica
        while True:
            try:
                await asyncio.wait_for(self.log_outs[replica].send(msg.SerializeToString()), SEND_TIMEOUT)
                break
            except asyncio.TimeoutError:
                logger.error("SENDING TIMED OUT, RETRYING")

    async def recv_msg(self, sock_num: int = 0) -> 'core_pb2.Request':
        msg = await self.zmq_ins[sock_num].recv()
        msg_pb = core_pb2.Request()
        msg_pb.ParseFromString(msg)
        self.msg_recv += 1
        # logger.debug(f"{get_hostname()} got msg: {msg_pb.request_id}")

        return msg_pb

    async def recv_log_msg(self):
        msg = await self.log_in.recv()

        msg_pb = core_pb2.LogEntry()
        msg_pb.ParseFromString(msg)
        return msg_pb

    def init_socket(self, socket: Socket):
        zmq_socket = socket.zmq(self.context)
        sock_path = '/tmp/'
        if socket.bind:
            if self.spec.native:
                ipc_sock = os.path.join(
                    sock_path, socket.host) + str(socket.port)

                if os.path.exists(ipc_sock):
                    os.remove(ipc_sock)

                conn_str = "ipc://{}".format(ipc_sock)
            else:
                conn_str = "tcp://*:{}".format(socket.port)
            zmq_socket.bind(conn_str)
            logger.info("{}: listening on {}".format(
                os.environ.get("HOSTNAME"), conn_str))
        else:
            if self.spec.native:
                ipc_sock = os.path.join(
                    sock_path, socket.host) + str(socket.port)
                conn_str = 'ipc://{}'.format(ipc_sock)
            else:
                conn_str = 'tcp://{}:{}'.format(socket.host, socket.port)
            zmq_socket.connect(conn_str)
            logger.info("{}: connecting to {}".format(
                self.spec.function_name, conn_str))

        if socket.sock_type == SocketType.SUB:
            zmq_socket.setsockopt(zmq.SUBSCRIBE, b'')
        zmq_socket.setsockopt(zmq.LINGER, 0)
        return zmq_socket

    def cleanup(self):
        for sock in [*self.zmq_ins, self.log_in, *self.log_outs]:
            if sock and not sock.closed:
                sock.close()

        for sock_list in self.zmq_out.values():
            for sock in sock_list:
                if not sock.closed:
                    sock.close()
