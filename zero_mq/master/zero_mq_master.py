import asyncio
import logging
from urllib.parse import ParseResultBytes


log = logging.getLogger('zero_mq_master.master')


class ZeroMQMaster(asyncio.Protocol):
    def data_received(self, data):
        print(data)
        print(ParseResultBytes(scheme='http', ))