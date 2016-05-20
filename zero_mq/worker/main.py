import os
import zmq
import logging


log = logging.getLogger('zero_mq_worker.main')
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

log.addHandler(ch)

HOST = '127.0.0.1'
PORT = 5555


def run(socket):
    while True:
        file_path = socket.recv_string()
        log.info('Recieved message: %r', file_path)

        if not os.path.exists(file_path) or os.path.isdir(file_path):
            log.error('%r is not a regular file', file_path)
            socket.send_json({
                'status': 'fail',
                'msg': 'Failed to open file',
            })
            continue

        with open(file_path, 'r') as fd:
            data = fd.read()

        log.debug('File\'s content: %r', data)
        socket.send_json({
            'status': 'ok',
            'msg': data,
        })


def main():
    log.info('Starting worker on host=%r, port=%r', HOST, PORT)
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.connect('tcp://{0}:{1}'.format(HOST, PORT))

    try:
        run(socket)
    except KeyboardInterrupt:
        log.info('Worker disabled')


if __name__ == '__main__':
    main()
