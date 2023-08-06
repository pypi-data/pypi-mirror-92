import datetime
import json
import logging
import os
import socket
import uuid
from json import JSONDecodeError
from threading import Thread

import pika
import sys
from pika.exceptions import ChannelWrongStateError, ConnectionWrongStateError

_LOGGER = logging.getLogger('cas.acabim.messaging')

NEW_IFC_PARSE_REQ_ENDPOINT = 'CAS:Ifc:ParseRequest:Parse:NEW'
NEW_IFC_VERIFY_REQ_ENDPOINT = 'CAS:Ifc:ParseRequest:Verify:NEW'
NEW_IFC_GENERATE_REQ_ENDPOINT = 'CAS:Ifc:Generate:NEW'
CANCEL_REQ_ENDPOINT = 'CAS:Ifc:ParseRequest:CANCEL'
STATUS_REQ_ENDPOINT = 'CAS:Ifc:ParseRequest:STATUS'

_EXPECTED_MSG_TYPE = {
    NEW_IFC_PARSE_REQ_ENDPOINT: 'ComplianceAuditSystems.Acabim.Messages.Bim:IfcParserProcessResponse',
    NEW_IFC_VERIFY_REQ_ENDPOINT: 'ComplianceAuditSystems.Acabim.Messages.Bim:IfcParserProcessResponse'
}


class MessagingHandler:
    def __init__(self, connection_name='cas.messaging.PythonClient'):
        self.current_status = {}
        self.connection_name = connection_name
        self.__pending_listeners = {}
        self.__create_connection()
        self.__create_thread()

    def __del__(self):
        self.stop()

    def __create_connection(self):
        if not hasattr(self, '__connection'):
            user_name = os.getenv('ACABIM_MESSAGING_USERNAME', 'guest')
            password = os.getenv('ACABIM_MESSAGING_PASSWORD', 'guest')
            host = os.getenv('ACABIM_MESSAGING_HOST', 'localhost')
            credentials = pika.PlainCredentials(user_name, password)
            params = pika.ConnectionParameters(host=host, credentials=credentials, retry_delay=10,
                                               connection_attempts=10,
                                               client_properties={
                                                   'connection_name': self.connection_name,
                                                   'hostname': socket.gethostname(),
                                                   'python_version': sys.version,
                                                   'process_id': os.getpid()
                                               })
            self.__connection = pika.SelectConnection(params, on_open_callback=self.__on_connected,
                                                      on_close_callback=self.__on_closed)

    def __create_thread(self):
        if not hasattr(self, '__bk_thread'):
            self.__bk_thread = Thread(target=self.__connect, name='cas.messaging.ConnectionHandler')
            self.__bk_thread.daemon = False

    def is_connected(self):
        return self.__connection.is_open if hasattr(self, '__connection') else False

    def start(self):
        if not self.is_connected():
            self.__create_connection()
            self.__create_thread()
            self.__bk_thread.start()

    def stop(self):
        self.__remove_connection()

    def listen(self, queue_name, callback):
        if callback is None:
            raise TypeError('callback cannot be none')

        if callback is not callable(callback):
            raise TypeError('expected callable function, not {0}'.format(type(callback)))

        self.__pending_listeners[queue_name] = callback
        self.__channel.exchange_declare(queue_name, exchange_type='fanout', durable=False,
                                        callback=lambda ex: self.__on_exchange_declared(ex, queue_name))

    def respond(self, req_queue_name, res_message_body, req_message):
        """ Respond with a message for a received request """
        if hasattr(self, '__channel'):
            res_queue = MessagingHandler.__get_response_queue_name(req_message)
            body = MessagingHandler.__create_response_message(req_queue_name, res_message_body, req_message)
            try:
                self.__channel.basic_publish(exchange=res_queue, routing_key='', body=body)
            except ChannelWrongStateError as e:
                _LOGGER.exception(e, 'Unable to send message - Channel not open')
        else:
            _LOGGER.error('No connection found to respond with the message')

    def __connect(self):
        _LOGGER.info('Starting connection')
        try:
            self.__connection.ioloop.start()
        except KeyboardInterrupt:
            self.__connection.close()

    def __remove_connection(self):
        """ Removes the connection and the channel after closing it """
        if hasattr(self, '__channel'):
            try:
                _LOGGER.debug('Channel going down')
                self.__channel.close()
                del self.__channel
            except ChannelWrongStateError:
                _LOGGER.warning('Unable to close channel - Channel may have already been closed')
                del self.__channel

        if hasattr(self, '__connection'):
            try:
                _LOGGER.debug('Connection going down')
                self.__connection.ioloop.add_callback_threadsafe(self.__connection.ioloop.stop)
                self.__connection.close()
                del self.__connection
            except ConnectionWrongStateError:
                _LOGGER.warning('Unable to close connection - connection may have already been closed')
                del self.__connection

        if hasattr(self, 'bk_thread'):
            _LOGGER.info('Waiting for the background thread to exit')
            self.__bk_thread.join()
            del self.__bk_thread

    def __on_connected(self, opened_connection):
        _LOGGER.info('Connection Opened with Host: %s', opened_connection.params.host)
        self.__connection.channel(on_open_callback=self.__on_channel_open)

    def __on_closed(self, closed_connection, exception):
        _LOGGER.exception(exception)
        _LOGGER.critical('Connection closed with Host: %s', closed_connection.params.host)
        self.__remove_connection()

    def __on_channel_open(self, opened_channel):
        _LOGGER.info('Channel open with Host: %s, Number: %s', opened_channel.connection.params.host,
                     opened_channel.channel_number)
        self.__channel = opened_channel

    def __on_exchange_declared(self, exchange, exchange_name):
        _LOGGER.debug('Exchange Declared - Message: %s, ExchangeName: %s', exchange.method.NAME, exchange_name)
        if exchange.method.NAME == 'Exchange.DeclareOk':
            _LOGGER.debug('Declaring Queue: %s', exchange_name)
            self.__channel.queue_declare(queue=exchange_name, durable=True,
                                         callback=lambda result: self.__on_queue_declared(result, exchange_name))
        else:
            _LOGGER.critical('Invalid exchange message - Unable to declare queue %s', exchange_name)
            raise Exception('Invalid Response when declaring exchange \'{0}\', Received: {1} '
                            .format(exchange_name, exchange.method.NAME))

    def __on_queue_declared(self, queue, queue_name):
        _LOGGER.debug('Queue Declared - Message: %s, QueueName: %s', queue.method.NAME, queue_name)
        if queue.method.NAME == 'Queue.DeclareOk':
            _LOGGER.debug('Binding Queue %s to exchange %s', queue_name, queue_name)
            self.__channel.queue_bind(exchange=queue_name, queue=queue_name, routing_key='',
                                      callback=lambda result: self.__on_queue_ready(result, queue_name))
        else:
            _LOGGER.critical('Invalid exchange message - Unable to bind queue %s', queue_name)
            raise Exception('Invalid Response when binding queue \'{0}\', Received: {1}'
                            .format(queue_name, queue.method.NAME))

    def __on_queue_ready(self, queue, queue_name):
        if queue.method.NAME == 'Queue.BindOk':
            _LOGGER.info('Queue Ready: %s', queue_name)
            if queue_name in self.__pending_listeners:  # if we have a pending listener that means we have to listen
                _LOGGER.info('Listener found for Queue: %s', queue_name)
                self.__channel.basic_consume(queue=queue_name, auto_ack=True,
                                             on_message_callback=lambda channel, method, properties, body:
                                             self.__on_new_message_received(queue_name, body))

    def __on_new_message_received(self, queue_name, body):
        content = MessagingHandler.__verify_and_get_message_content(body)
        if queue_name in self.__pending_listeners:
            self.__pending_listeners[queue_name](content)

    @staticmethod
    def __verify_and_get_message_content(body):
        try:
            return json.loads(body)
        except JSONDecodeError:
            _LOGGER.critical('Unhandled Body content: Invalid Message - Unable to parse JSON')
            _LOGGER.critical('Body: "%s"', body.decode('utf8'))
            _LOGGER.exception(JSONDecodeError)

    @staticmethod
    def __get_response_queue_name(req_message_content):
        return req_message_content['responseAddress'].split('/').pop().split('?')[0]

    @staticmethod
    def __create_response_message(req_queue_name, response_message_content, req_message):
        res_message = {'messageId': str(uuid.uuid4())}
        if 'requestId' in req_message:
            res_message['requestId'] = req_message['requestId']

        if 'conversationId' in req_message:
            res_message['conversationId'] = req_message['conversationId']

        if req_queue_name in _EXPECTED_MSG_TYPE:
            res_message['messageType'] = ['urn:message:{0}'.format(_EXPECTED_MSG_TYPE[req_queue_name])]
        else:
            _LOGGER.warning('No message_type found, Message will not be accepted by MassTransit if no type is provided')

        res_message['message'] = response_message_content
        res_message['sentTime'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        res_message['host'] = MessagingHandler.__get_host_info()
        return bytes(json.dumps(res_message), 'utf8')

    @staticmethod
    def __is_response_message(content):
        return 'message' in content and 'sentTime' in content and 'host' in content

    @staticmethod
    def __get_host_info():
        return {'machineName': socket.gethostname(),
                'processName': 'ifcparser',
                'processId': os.getpid(),
                'pythonVersion': sys.version
                }