import logging
import os
import socket
from threading import Thread

import pika
import sys
from pika.exceptions import ChannelWrongStateError

_LOGGER = logging.getLogger('cas.acabim.messaging')


def __create_connection():
    user_name = os.getenv('ACABIM_MESSAGING_USERNAME', 'guest')
    password = os.getenv('ACABIM_MESSAGING_PASSWORD', 'guest')
    host = os.getenv('ACABIM_MESSAGING_HOST', 'localhost')
    credentials = pika.PlainCredentials(user_name, password)
    params = pika.ConnectionParameters(host=host, credentials=credentials, retry_delay=10,
                                       connection_attempts=10,
                                       client_properties={
                                           'connection_name': 'cas.ifcparser.client',
                                           'hostname': socket.gethostname(),
                                           'python_version': sys.version,
                                           'process_id': os.getpid()
                                       })

    return pika.SelectConnection(params, on_open_callback=__on_connection_open,
                                 on_close_callback=__on_connection_closed)


def __on_connection_open(opened_connection):
    _LOGGER.info('Connection Opened with Host: %s', opened_connection.params.host)
    opened_connection.channel(on_open_callback=__on_channel_open)


def __on_connection_closed(closed_connection, exception):
    _LOGGER.exception(exception)
    _LOGGER.critical('Connection closed with Host: %s', closed_connection.params.host)
    _LOGGER.info('Attempting to reconnect with %s', closed_connection.params.host)


def __on_channel_open(opened_channel):
    _LOGGER.info('Channel open with Host: %s, Number: %s', opened_channel.connection.params.host,
                 opened_channel.channel_number)
    global _CHANNEL
    _CHANNEL = opened_channel


def __on_exchange_declared(exchange, exchange_name):
    _LOGGER.debug('Exchange Declared - Message: %s, ExchangeName: %s', exchange.method.NAME, exchange_name)
    if exchange.method.NAME == 'Exchange.DeclareOk':
        _LOGGER.debug('Declaring Queue: %s', exchange_name)
        _CHANNEL.queue_declare(queue=exchange_name, durable=True,
                               callback=lambda result: __on_queue_declared(result, exchange_name))
    else:
        _LOGGER.critical('Invalid exchange message - Unable to declare queue %s', exchange_name)
        raise Exception('Invalid Response when declaring exchange \'{0}\', Received: {1} '
                        .format(exchange_name, exchange.method.NAME))


def __on_queue_declared(queue, queue_name):
    _LOGGER.debug('Queue Declared - Message: %s, QueueName: %s', queue.method.NAME, queue_name)
    if queue.method.NAME == 'Queue.DeclareOk':
        _LOGGER.debug('Binding Queue %s to exchange %s', queue_name, queue_name)
        _CHANNEL.queue_bind(exchange=queue_name, queue=queue_name, routing_key='',
                            callback=lambda result: __on_queue_ready(result, queue_name))
    else:
        _LOGGER.critical('Invalid exchange message - Unable to bind queue %s', queue_name)
        raise Exception('Invalid Response when binding queue \'{0}\', Received: {1}'
                        .format(queue_name, queue.method.NAME))


def __on_queue_ready(queue, queue_name):
    if queue.method.NAME == 'Queue.BindOk':
        _LOGGER.info('Queue Ready: %s', queue_name)
        if queue_name in _PENDING_LISTENERS:
            listener = _PENDING_LISTENERS[queue_name]
            _CHANNEL.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=listener)
            _LOGGER.info('Started listening to %s', queue_name)
            del _PENDING_LISTENERS[queue_name]
    pass


_CONNECTION = __create_connection()
_CHANNEL = None
_EXECUTING_THREAD = None
_PENDING_LISTENERS = {}


def connect():
    global _EXECUTING_THREAD
    _EXECUTING_THREAD = Thread(target=__connect, name='cas.acabim.messaging.connectionHandler')
    _EXECUTING_THREAD.daemon = False
    _EXECUTING_THREAD.start()


def __connect():
    _LOGGER.info('Starting connection')

    try:
        _CONNECTION.ioloop.start()
    except Exception as e:
        _LOGGER.exception(e)


def disconnect():
    global _CHANNEL
    try:
        if _CHANNEL is not None:
            _CHANNEL.close()
            _CHANNEL = None
    except ChannelWrongStateError:
        _LOGGER.warning('Unable to close channel - Channel may have already been closed')


def listen(queue_name, on_new_msg_callback):
    if on_new_msg_callback is None:
        raise TypeError("on_new_msg_callback cannot be None")

    if not callable(on_new_msg_callback):
        raise TypeError('expected callable function, not {0}'.format(type(on_new_msg_callback)))

    while True:
        if _CHANNEL is not None:
            break

    _PENDING_LISTENERS[queue_name] = on_new_msg_callback
    _CHANNEL.exchange_declare(queue_name, 'fanout', durable=True,
                              callback=lambda ex: __on_exchange_declared(ex, queue_name))
