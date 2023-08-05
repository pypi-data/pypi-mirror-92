#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pinecone.functions import Function
from pinecone.runnable import Runnable
from pinecone.network.zmq import Socket, SocketType, ServletSpec, entrypoints
from pinecone.network.selector.shards import ShardSelector
from pinecone.utils.constants import ZMQ_PORT_IN, ZMQ_LOG_PORT, ZMQ_CONTROL_PORT
from pinecone.utils import tracing, load_hub_service, module_name, replica_name, parse_hostname, replica_kube_hostname, get_hostname
from pinecone.utils.wal import WAL
from pinecone.protos import core_pb2

import concurrent.futures
import asyncio
import json
from typing import Dict, List, Optional, Callable, Awaitable
from pydoc import locate
import os
import random
import importlib
import argparse
import traceback

from loguru import logger
from ddtrace import tracer
from ddtrace.tracer import Context
from ddtrace.contrib.asyncio import run_in_executor


class ZMQService(Runnable):

    @classmethod
    def from_args(cls, args):
        """
        :param functions:
        :param args:
        :return:
        """
        # logger.warning("loading {functions}", functions=args.function)
        if args.function in ['pinecone.functions.model.transformer.hub.HubTransformer',
                             'pinecone.functions.model.scorer.hub.HubScorer',
                             'pinecone.functions.model.HubFunction']:

            model = importlib.import_module('model')
            service_cls = load_hub_service(model)
            logger.info('loaded functions class {cls}', cls=service_cls)
            args.config = json.dumps(
                {k: v for k, v in json.loads(args.config).items() if k != 'image'})
        else:
            service_cls = locate(args.function)
        service = service_cls.from_args(args)
        return cls(service, json.loads(args.next), args.service, native=args.native)

    def to_args(self):
        """
        Return the command line args to run this instance
        :return:
        """
        return ['pinecone.functions',
                '--function', module_name(self.function),
                '--next', json.dumps(self.next_services,
                                     separators=(',', ':')),
                '--service', self.service_name,
                *(['--native'] if self.native else []),
                *self.function.to_args()]

    @classmethod
    def add_args(cls, parser: argparse.ArgumentParser):
        parser.add_argument('--function', type=str,
                            help='module of functions class to run')
        parser.add_argument('--next', type=str,
                            help='mapping of next functions in the DAG')
        parser.add_argument('--native', action='store_true')
        parser.add_argument('--service', type=str,
                            help='name of the running runner')
        Function.add_args(parser)

    @classmethod
    def start_with_args(cls, args):
        servlet = cls.from_args(args)
        servlet.start()

    def __init__(self, function: Function, next_services: Dict[str, List[str]], service_name: str, native=True):
        """
        :param service: The functions to mount with a ZMQServlet
        :param next: The next functions in the DAG
        """

        self.function = function
        self.executor = None
        self.next_services = next_services
        self.native = native
        self.service_name = service_name

    def log_out_socks(self, shard_id: int):
        if self.function.volume_request is not None:
            return [
                Socket(False, SocketType.PUSH,
                       host=replica_name(self.function.name, shard_id, replica_id=replica_id) if self.native
                       else replica_kube_hostname(self.function.name, shard_id, replica_id),
                       port=ZMQ_LOG_PORT)
                for replica_id in range(0, self.replicas)]

    def log_in_socket(self):
        return Socket(True, SocketType.PULL, ZMQ_LOG_PORT, host=get_hostname())

    def get_sockets(self):
        out_type = self.function.out_sock_type
        in_type = self.function.in_sock_type

        in_sockets = [Socket(True, in_type,
                             host=get_hostname(),
                             port=ZMQ_PORT_IN)]

        out_sockets = {r: [Socket(False, out_type, host=s, port=ZMQ_PORT_IN) for s in n] for r, n in
                       self.next_services.items() if n}

        return in_sockets, out_sockets

    async def handle_msg_with_wal(self, msg: 'core_pb2.Request', hostname: str, wal: WAL, offset=None):
        req_type = msg.WhichOneof('body')
        use_wal = req_type in ['index', 'delete'] and self.function.volume_request is not None
        if use_wal:
            new_offset = await wal.put(msg, offset=offset)
            if new_offset is None:
                return

        loop = asyncio.get_event_loop()
        if self.executor is None:
            self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        try:
            result = await run_in_executor(loop, self.executor, self.function.handle_msg, msg)
            if use_wal:
                await wal.set_client_offset(msg.client_id, msg.client_offset)
                await wal.ack(new_offset)
            return result
        except Exception as e:
            msg.status.code = core_pb2.Status.StatusCode.ERROR
            details = core_pb2.Status.Details(function=self.name,
                                              function_id=str(hostname),
                                              exception=str(e),
                                              traceback=traceback.format_exc())
            details.time.GetCurrentTime()
            msg.status.details.append(details)
            logger.error(details.traceback)
            return msg

    def get_call_handler(self, hostname: str, wal: WAL):
        async def call_handler(msg: 'core_pb2.Request', offset=None):
            msg_context = Context(trace_id=msg.telemetry_trace_id, span_id=msg.telemetry_parent_id)
            tracer.context_provider.activate(msg_context)
            with tracer.trace(self.function.__class__.__name__) as span:
                tracing.set_span_tags(span, msg)
                msg.telemetry_parent_id = span.span_id
                result = await self.handle_msg_with_wal(msg, hostname, wal, offset)
                return result

        return call_handler

    async def proxy_msg(self, msg):
        return msg

    def get_handle_log_msg(self, call_handler: Callable[['core_pb2.Request', Optional[int]],
                                                        Awaitable['core_pb2.Request']], replica_id: int,
                           wal: WAL):
        async def handle_log_msg(msg: 'core_pb2.LogEntry'):
            if replica_id > 0:
                # logger.debug(f"{get_hostname()} GOT LOG MSG {msg.offset}, OFFSETS:{wal.offsets_list()}")
                await call_handler(msg.entry, msg.offset)
            else:
                await wal.remote_ack(msg.offset, msg.ack.replica, msg.ack.replay)

        return handle_log_msg

    def start(self, hostname=None):
        # FORMAT: <function.name>-s<shard_id>-r<replica_id>]
        if hostname:
            os.environ['HOSTNAME'] = hostname
        hostname = get_hostname()

        if hostname is None:
            raise RuntimeError('Must set HOSTNAME to run 0mq service')

        parsed_shard, parsed_replica = parse_hostname(self.name, hostname)

        # XXX[Fei]: chance of collision?
        replica_id = random.randint(1, 999999) if parsed_replica is None else parsed_replica
        shard_id = 0 if parsed_shard is None else parsed_shard
        logger.debug(f"PARSED SHARD: {shard_id}, PARSED REPLICA: {replica_id} hostname: {hostname}")

        self.function.id = replica_id
        in_sockets, out_sockets = self.get_sockets()

        if self.volume_request:
            wal = WAL(replica_id, self.function.replicas, os.path.join(self.function.default_persistent_dir, 'wal'))
        else:
            wal = None

        selector = ShardSelector()
        handler = self.get_call_handler(hostname, wal)

        servlet_spec = ServletSpec(handler, in_sockets, out_sockets, selector, self.native,
                                   replica_name(self.function.name, shard_id), shard_id, replica_id,
                                   self.function.get_stats,
                                   service_name=self.service_name,
                                   log_out_sockets=self.log_out_socks(shard_id),
                                   log_in_socket=self.log_in_socket(),
                                   handle_log_msg=self.get_handle_log_msg(handler, replica_id, wal))

        self.function.setup()
        if wal is not None:
            logger.warning(f"SIZE BEFORE REPLAY: {self.function.get_stats()} for {hostname}")
            wal.write_offset(replica_id, 0)  # replay all the messages
            request_backlog = list(wal.load_sync(self.function.handle_msg))
            logger.warning(f"SIZE AFTER REPLAY: {self.function.get_stats()} "
                           f"REQ BACKLOG: {len(request_backlog)} for {hostname}")
        entrypoints.start(servlet_spec, wal=wal)

    def cleanup(self):
        self.function.cleanup()

    @property
    def name(self):
        return self.function.name

    @property
    def image(self):
        return self.function.image

    @property
    def replicas(self) -> int:
        return self.function.replicas

    @property
    def shards(self) -> int:
        return self.function.shards

    @property
    def ports(self) -> List[int]:
        return [ZMQ_PORT_IN, ZMQ_LOG_PORT, ZMQ_CONTROL_PORT]

    @property
    def ext_port(self) -> Optional[int]:
        return

    @property
    def memory_request(self) -> int:
        return self.function.memory_request

    @property
    def volume_request(self) -> Optional[int]:
        return self.function.volume_request
