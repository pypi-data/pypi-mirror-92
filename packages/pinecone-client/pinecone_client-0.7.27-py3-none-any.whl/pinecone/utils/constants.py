#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

import os

MAX_CLIENTS = 100
MAX_RETRY_MSG = 100
RETRY_SECONDS = 2
GATEWAY_NAME = 'gatewayrouter'
MAX_MSG_SIZE = 100 * 1024 * 1024
OUT_POOL_SIZE = 10

ZMQ_CONTROL_PORT = os.environ.get('ZMQ_CONTROL_PORT', 5559)
ZMQ_PORT_IN = os.environ.get('ZMQ_PORT_IN', 5557)
ZMQ_LOG_PORT = os.environ.get('ZMQ_LOG_PORT', 5558)
PC_CONTROLLER_PORT = os.environ.get('PC_CONTROLLER_PORT', 8083)
SERVICE_GATEWAY_PORT = os.environ.get('SERVICE_GATEWAY_PORT', 5007)
PERSISTENT_VOLUME_MOUNT = '/data'
ENV_VARS = [ZMQ_CONTROL_PORT, ZMQ_PORT_IN, ZMQ_LOG_PORT, PC_CONTROLLER_PORT]
ZMQ_SECONDARY_PORT = 5559

MEMORY_LIMIT_MB = int(os.environ.get("PINECONE_MEMORY_LIMIT_MB", default="0"))  # default is 0 - no limit
MAX_ID_LENGTH = 64
