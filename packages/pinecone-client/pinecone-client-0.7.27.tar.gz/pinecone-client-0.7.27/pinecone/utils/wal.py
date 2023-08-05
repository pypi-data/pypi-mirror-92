#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pinecone.protos import core_pb2
from pinecone.network.zmq import ZMQServlet
from pinecone.utils import open_or_create, get_hostname
from pinecone.utils.constants import MAX_CLIENTS

from typing import Optional, Iterable, Tuple
from loguru import logger
import google.protobuf.message

import concurrent.futures
from threading import Lock
import asyncio
import os
import functools
import mmap

OFFSET_BYTES = 8
SIZE_BYTES = 4
BYTEORDER = 'big'


class WAL:

    def __init__(self, replica: int, num_replicas: int, path: str):
        self.replica = replica
        self.num_replicas = num_replicas

        self.servlet = None  # type: Optional[ZMQServlet]
        self.executor = concurrent.futures.ThreadPoolExecutor()

        os.makedirs(path, exist_ok=True)

        log_path = os.path.join(path, 'log')
        self.log_file = open_or_create(log_path)
        self.log_lock = Lock()

        self.last = None
        self.size = self.load_size()

        offset_path = os.path.join(path, 'offsets')
        self.offset_file = open_or_create(offset_path, truncate=OFFSET_BYTES*self.num_replicas)
        self.offsets = mmap.mmap(self.offset_file.fileno(), 0)
        self.offset_locks = [Lock() for _ in range(0, self.num_replicas)]

        client_offsets_path = os.path.join(path, 'client_offsets')
        self.client_offsets_file = open_or_create(client_offsets_path, truncate=OFFSET_BYTES*MAX_CLIENTS)

        self.client_offsets = mmap.mmap(self.client_offsets_file.fileno(), 0)
        self.client_offsets_locks = [Lock() for _ in range(0, MAX_CLIENTS)]

    def load_size(self):
        size = 0
        for pos, entry in self.sync_replay_log(0):
            size += 1
            self.last = entry
        return size

    def cleanup(self):
        self.offset_file.close()
        self.log_file.close()

    @property
    def leader(self):
        return self.replica == 0

    async def run_sync(self, func, *args):
        return await asyncio.get_event_loop().run_in_executor(self.executor, functools.partial(func, *args))

    def get_offset(self, replica: int):
        start = OFFSET_BYTES * replica
        return int.from_bytes(self.offsets[start:start + OFFSET_BYTES], BYTEORDER)

    def offsets_list(self):
        return [self.get_offset(replica) for replica in range(0, self.num_replicas)]

    def write_offset(self, replica: int, offset: int):
        with self.offset_locks[replica]:
            self.offsets.seek(replica*OFFSET_BYTES)
            self.offsets.write(offset.to_bytes(OFFSET_BYTES, BYTEORDER))
            self.offsets.flush()

    async def set_offset(self, replica: int, offset: int):
        await self.run_sync(self.write_offset, replica, offset)

    def get_client_offset(self, client_id: int):
        if client_id >= MAX_CLIENTS:
            return 0
        with self.client_offsets_locks[client_id]:
            start = client_id * OFFSET_BYTES
            return int.from_bytes(self.client_offsets[start:start + OFFSET_BYTES], BYTEORDER)

    def is_next(self, client_id: int, client_offset: int):
        if self.leader:
            if client_offset == 0:
                self.sync_set_client_offset(client_id, 0)
            return client_offset == self.get_client_offset(client_id) + 1 or client_offset == 0
        else:
            return True

    def sync_set_client_offset(self, client_id: int, client_offset: int):
        if client_id >= MAX_CLIENTS:
            return
        with self.client_offsets_locks[client_id]:
            start = client_id * OFFSET_BYTES
            self.client_offsets[start:start + OFFSET_BYTES] = client_offset.to_bytes(OFFSET_BYTES, BYTEORDER)
            self.client_offsets.flush()

    async def set_client_offset(self, client_id: int, client_offset: int):
        if self.get_client_offset(client_id) > client_offset:
            return
        await self.run_sync(self.sync_set_client_offset, client_id, client_offset)

    def sync_put(self, entry: core_pb2.Request, offset: int):
        if not offset or self.size == offset:
            with self.log_lock:
                self.log_file.seek(0, os.SEEK_END)
                entry_bytes = entry.SerializeToString()
                size = len(entry_bytes).to_bytes(SIZE_BYTES, BYTEORDER)
                self.log_file.write(size + entry_bytes)

                self.size += 1
                self.last = entry
        else:
            return
        return self.size - 1

    async def put(self, item: core_pb2.Request, offset: int = None):
        if not self.leader and offset is None:
            raise RuntimeError(f"{get_hostname()} Attempted to write directly to replica {self.replica} instead of leader")
        return await self.run_sync(self.sync_put, item, offset)

    def read_entry(self):
        size = int.from_bytes(self.log_file.read(SIZE_BYTES), BYTEORDER)
        msg_bytes = self.log_file.read(size)
        entry = core_pb2.Request()
        try:
            entry.ParseFromString(msg_bytes)
        except google.protobuf.message.DecodeError:
            logger.debug(msg_bytes)
        return entry, msg_bytes

    def sync_replay_log(self, offset: int) -> Iterable[Tuple[int, core_pb2.Request]]:
        with self.log_lock:
            self.log_file.seek(0)
            pos = 0
            while True:
                entry, msg_bytes = self.read_entry()

                if msg_bytes == b'':
                    break
                if pos >= offset:
                    yield pos, entry
                pos += 1

    def get_leader_log_backlog(self, replica: int) -> Iterable[core_pb2.LogEntry]:
        return [core_pb2.LogEntry(entry=entry, offset=offset)
                for offset, entry in self.sync_replay_log(self.get_offset(replica))]

    def sync_ack(self, offset: int):
        self.write_offset(self.replica, offset)

    async def ack(self, offset: int):
        prev_offset = self.get_offset(self.replica)
        if prev_offset > offset:
            logger.warning('Acked offset less than current offset')
        # elif prev_offset + 1 > offset:
        #     logger.warning('Acked by more than one offset')

        await self.set_offset(self.replica, offset)

        if self.leader:
            for r in range(1, self.num_replicas):
                msg = core_pb2.LogEntry(entry=self.last, offset=offset)
                await self.servlet.send_log_msg(msg, r)
        else:
            ack = core_pb2.Ack(replica=self.replica)
            await self.servlet.send_log_msg(core_pb2.LogEntry(offset=offset, ack=ack), 0)

    async def remote_ack(self, start_offset: int, replica: int, replay=False):
        if replay:
            logs = await self.run_sync(lambda s: list(self.sync_replay_log(s)), start_offset + 1)
            if not self.get_offset(self.replica) == len(logs) + start_offset:
                logger.error(f"INCORRECT LENGTH OF REPLAY LOG {len(logs)} OFFSETS: {self.offsets_list()}. Size {self.size}")
            for offset, msg in logs:
                await self.servlet.send_log_msg(core_pb2.LogEntry(entry=msg, offset=offset), replica)

    def get_replay_request(self):
        ack = core_pb2.Ack(replica=self.replica, replay=True)
        return core_pb2.LogEntry(offset=self.get_offset(self.replica), ack=ack)

    def load_sync(self, handler):
        logger.info(f'Recovering from local WAL: offset: {self.get_offset(self.replica)}')
        for offset, entry in self.sync_replay_log(self.get_offset(self.replica)):
            response = handler(entry)  # type: core_pb2.Request
            self.sync_ack(offset)
            if self.leader:
                yield response
