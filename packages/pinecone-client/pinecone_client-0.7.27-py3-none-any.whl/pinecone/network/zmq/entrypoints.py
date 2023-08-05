#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pinecone.protos import core_pb2
from pinecone.utils.exceptions import RestartException
from pinecone.network.zmq.spec import ServletSpec
from pinecone.network.zmq import ZMQServlet, RECV_TIMEOUT

from loguru import logger
import asyncio
from typing import Awaitable, Callable, List


def start(servlet_spec: ServletSpec, wal=None):
    logger.info('starting zmq servlet: %s ' % servlet_spec.function_name)

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    servlet = ZMQServlet(servlet_spec)

    if wal is not None:
        wal.servlet = servlet
        loop.create_task(servlet.consume_msgs())

    servlet.wal = wal

    loop.create_task(servlet.poll())
    loop.create_task(servlet.heartbeat())
    loop.run_forever()
    if servlet.exception is not None and type(servlet.exception) == RestartException:
        raise RestartException


def run_in_servlet(servlet_spec: ServletSpec, function: Callable[..., Awaitable], *args):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    servlet = ZMQServlet(servlet_spec)
    result = asyncio.run(function(servlet, *args))
    loop.stop()
    return result


async def recv_requests(servlet: ZMQServlet, num: int):
    msgs = []
    while len(msgs) < num:
        try:
            msgs.append(await asyncio.wait_for(servlet.recv_msg(), RECV_TIMEOUT))
            logger.success(msgs[-1])
        except asyncio.TimeoutError:
            logger.error('timed out')
            continue
    return msgs


async def recv_logs(servlet: ZMQServlet, num: int):
    msgs = []
    while len(msgs) < num:
        try:
            msgs.append(await asyncio.wait_for(servlet.recv_log_msg(), RECV_TIMEOUT))
        except asyncio.TimeoutError:
            continue
    return msgs


async def send_logs(servlet: ZMQServlet, log: List['core_pb2.LogEntry'], replica: int):
    for msg in log:
        await servlet.send_log_msg(msg, replica)


async def send_requests(servlet: ZMQServlet, requests: List['core_pb2.Request']):
    for msg in requests:
        await servlet.send_msg(msg)
