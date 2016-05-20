"""
Процесс слушает на порту 8080 по протоколу HTTP с помощью TCP-сокета.
При поступлении HTTP-запроса из извлекается URI извлекается путь и передается
свободному worker-у. После получения ответа от worker-а, формируется
HTTP-ответ.

Usage: python3.5 main.py
"""
import zmq
import logging

from http_parser import pyparser


log = logging.getLogger('zero_mq_master.main')
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

log.addHandler(ch)

WEB_PORT = 8080
WORKER_PORT = 5555


def parse_http_request(data):
    print(data)
    parser = pyparser.HttpParser()
    parser.execute(data, len(data))
    path = parser.get_path()
    return path


def gen_response(data):
    if data['status'] == 'fail':
        return 'HTTP/1.1 404 Not Found\nContent-Type: text/html'

    if data['status'] == 'ok':
        return 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n{0}'.format(data['msg'])

    raise RuntimeError('Unknown data format')


def main():
    log.info('Start master')
    context = zmq.Context()

    web_socket = context.socket(zmq.ROUTER)
    worker_socket = context.socket(zmq.DEALER)
    web_socket.bind('tcp://*:{0}'.format(WEB_PORT))
    worker_socket.bind('tcp://*:{0}'.format(WORKER_PORT))

    poller = zmq.Poller()
    poller.register(web_socket, zmq.POLLIN)
    poller.register(worker_socket, zmq.POLLIN)

    log.info('Start main loop')
    while True:
        socks = dict(poller.poll())

        if socks.get(web_socket) == zmq.POLLIN:
            data = web_socket.recv_multipart()
            print(data)
            log.debug('Data recieved: %r', data)
            # print(parse_http_request(data))
            # worker_socket.send_multipart(parse_http_request(data))

        if socks.get(worker_socket) == zmq.POLLIN:
            data = worker_socket.recv_json()
            web_socket.send_string('HTTP/1.1 200 OK\nContent-Type: text/html\n\n')


if __name__ == '__main__':
    main()
