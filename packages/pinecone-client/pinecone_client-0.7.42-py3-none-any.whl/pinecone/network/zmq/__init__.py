#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#
from pinecone.protos import core_pb2
from pinecone.utils import constants
from pinecone.utils import get_hostname, replica_kube_hostname, replica_name, tracing
from pinecone.network.zmq.spec import ServletSpec, SocketType, Socket

from loguru import logger
from ddtrace import tracer
from ddtrace.tracer import Context

import asyncio
import zmq
import zmq.asyncio
import os
import random
import itertools


class ZMQServlet:

    def __init__(self, servlet_spec: ServletSpec):
        self.spec = servlet_spec
        self.context = zmq.asyncio.Context()
        self.total_socks = 0

        self.exception = None
        if len(self.spec.in_sockets) > 0:
            self.zmq_ins = [self.init_socket(in_sock)
                            for in_sock in self.spec.in_sockets]

        self._bind_outs = dict()
        self._zmq_out_pool = [self.zmq_out_socks(i == 0) for i in range(0, constants.OUT_POOL_SIZE)
                              if self.total_socks < constants.MAX_SOCKS_OPEN]
        self.out_pool_size = len(self._zmq_out_pool)

        self.msg_sent = 0
        self.msg_recv = 0
        self.gateway_outs = []
        self.gateway_control = {}

    def gateway_control_sock(self, replica: int) -> zmq.Socket:
        if replica not in self.gateway_control:
            self.gateway_control[replica] = self.init_socket(Socket(False, SocketType.PUSH,
                                                                    constants.ZMQ_CONTROL_PORT,
                                                                    host=self.gateway_host(replica)))
        return self.gateway_control[replica]

    def get_bind_out(self, s: Socket) -> zmq.Socket:
        assert s.bind
        if s.port not in self._bind_outs:
            self._bind_outs[s.port] = self.init_socket(s)
        return self._bind_outs[s.port]

    def zmq_out_socks(self, do_writes: bool):
        return {r: [self.get_bind_out(s) if s.bind else self.init_socket(s) for s in sockets
                    if (r != 'write' or do_writes)]
                for r, sockets in self.spec.out_sockets.items()}

    @property
    def pretty_name(self) -> str:
        return self.spec.function_name + " shard:" + str(self.spec.shard) + " replica:" + str(self.spec.replica)

    async def handle_msg(self, msg: core_pb2.Request):
        route = core_pb2.Route(function=get_hostname(), function_id=self.spec.shard)
        route.start_time.GetCurrentTime()

        msg_context = Context(trace_id=msg.telemetry_trace_id, span_id=msg.telemetry_parent_id)
        tracer.context_provider.activate(msg_context)
        with tracer.trace(self.spec.function_name) as span:
            tracing.set_span_tags(span, msg)
            msg.telemetry_parent_id = span.span_id
            if self.spec.handle_msg:
                response = await self.spec.handle_msg(msg)
                route.end_time.GetCurrentTime()
                msg.routes.append(route)
                if response:
                    if self.spec.shard != 0:
                        response.shard_num = self.spec.shard
                    await self.send_msg(response)

    async def poll_sock(self, sock: zmq.Socket):
        while True:
            try:
                msg = await asyncio.wait_for(self.recv_msg(sock), constants.RECV_TIMEOUT)
                await self.handle_msg(msg)
            except asyncio.TimeoutError:
                pass

    async def poll(self):
        loop = asyncio.get_running_loop()
        await asyncio.gather(*(loop.create_task(self.poll_sock(sock)) for sock in self.zmq_ins))

    def gateway_host(self, replica: int):
        return replica_name(constants.GATEWAY_NAME, 0, replica) if self.spec.native \
            else replica_kube_hostname(constants.GATEWAY_NAME, 0, replica)

    def get_gateway_sock(self, gateway_num: int, sock: Socket) -> zmq.Socket:
        while gateway_num >= len(self.gateway_outs):
            new_sock = Socket(sock.bind, sock_type=sock.sock_type, port=sock.port,
                              host=self.gateway_host(len(self.gateway_outs)))
            self.gateway_outs.append(self.init_socket(new_sock))
        return self.gateway_outs[gateway_num]

    async def send_msg(self, msg: 'core_pb2.Request'):
        self.msg_sent += 1
        send_sockets = []
        for path in {msg.path, '*'}:
            for sock in (sock for sock in self.spec.out_sockets.get(path, []) if sock.host == constants.GATEWAY_NAME):
                send_sockets.append(self.get_gateway_sock(msg.gateway_num, sock))
                break
            else:
                socket_idx = 0 if msg.path == 'write' else random.randint(0, self.out_pool_size - 1)
                zmq_out_sockets = self._zmq_out_pool[socket_idx]
                send_sockets.extend(zmq_out_sockets.get(path, []))
                # logger.error(f"{os.environ.get('HOSTNAME')}: send socks: {[sock.host for sock in self.spec.out_sockets.get(path, [])]}")

        if len(send_sockets) == 0:
            logger.warning('{}: no out socket for path {}'.format(get_hostname(), msg.path))

        shard_msgs = self.spec.out_socket_selector.select_socket(msg, len(send_sockets))
        for socket, shard_msg in zip(send_sockets, shard_msgs):
            if shard_msg is not None:
                await socket.send(shard_msg.SerializeToString())

        if msg.traceroute:
            receipt = core_pb2.TraceRoute(request_id=msg.request_id, client_id=msg.client_id,
                                          client_offset=msg.client_offset, routes=msg.routes)
            await self.gateway_control_sock(msg.gateway_num).send(receipt.SerializeToString())

    async def recv_msg(self, sock: zmq.Socket) -> 'core_pb2.Request':
        msg = await sock.recv()
        msg_pb = core_pb2.Request()
        msg_pb.ParseFromString(msg)
        self.msg_recv += 1
        return msg_pb

    def init_socket(self, socket: Socket):
        zmq_socket = socket.zmq(self.context)
        zmq_socket.set_hwm(constants.MAX_MSGS_PENDING)  # needs to be set before bind/connect
        zmq_socket.setsockopt(zmq.RCVBUF, 2 * constants.MAX_MSG_SIZE)
        zmq_socket.setsockopt(zmq.SNDBUF, 2 * constants.MAX_MSG_SIZE)
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
            logger.info("{}: listening on {}".format(self.pretty_name, conn_str))
        else:
            if self.spec.native:
                ipc_sock = os.path.join(
                    sock_path, socket.host) + str(socket.port)
                conn_str = 'ipc://{}'.format(ipc_sock)
            else:
                conn_str = 'tcp://{}:{}'.format(socket.host, socket.port)
            zmq_socket.connect(conn_str)
            logger.info("{}: connecting to {}".format(
                self.pretty_name, conn_str))

        if socket.sock_type == SocketType.SUB:
            zmq_socket.setsockopt(zmq.SUBSCRIBE, b'')
        zmq_socket.setsockopt(zmq.LINGER, 0)
        self.total_socks += 1
        return zmq_socket

    @property
    def all_socks(self):
        return itertools.chain(self.zmq_ins, *[sum(zmq_out.values(), []) for zmq_out in self._zmq_out_pool])

    def cleanup(self):
        for sock in self.all_socks:
            if sock and not sock.closed:
                sock.close()
