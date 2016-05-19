"""
Процесс слушает на порту 8080 по протоколу HTTP с помощью TCP-сокета.
При поступлении HTTP-запроса из извлекается URI извлекается путь и передается
свободному worker-у. После получения ответа от worker-а, формируется
HTTP-ответ.

Usage: python3.5 main.py
"""
import socket
import asyncio
import logging

from zero_mq.master.zero_mq_master import ZeroMQMaster


log = logging.getLogger('zero_mq_master.main')
log.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

log.addHandler(ch)

HOST = '0.0.0.0'
PORT = 8080


def main():
    log.info('Start master')
    loop = asyncio.get_event_loop()

    future = loop.create_server(ZeroMQMaster, host=HOST, port=PORT)
    srv = loop.run_until_complete(future)
    log.info('Master server created. Socket: %r', srv.sockets[0].getsockname())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        log.info('Master off')

if __name__ == '__main__':
    main()
