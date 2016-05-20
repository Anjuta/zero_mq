import zmq
import asyncio
import logging

from http_parser import pyparser


log = logging.getLogger('zero_mq_master.master')


class ZeroMQMaster(asyncio.Protocol):
    def __init__(self, host='localhost', port=5555):
        self.parser = pyparser.HttpParser()

        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect('tcp://{0}:{1}'.format(host, port))

    def data_received(self, data):
        """
        При получении запроса, из него извлекается путь и передается свободному
        worker-у.
        """
        print(dir(self))
        log.debug('Data recieved: %r', data)
        self.parser.execute(data, len(data))
        path = self.parser.get_path()
        log.info('Recieved message with path: %r', path)
        self.socket.send_string(path)

        resp = self.socket.recv_json()
        log.info('Recieved message: %r', resp)
        if resp['status'] == 'fail':
            return 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'

