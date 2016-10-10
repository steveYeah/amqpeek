"""
Connecting to, and monitoring of RMQ
"""
import logging
import time

from pika import PlainCredentials, BlockingConnection, ConnectionParameters
from pika.exceptions import AMQPConnectionError


class Connector(object):
    """
    Abstracted connection to RMQ.

    Holds credentials for continued connection drop and reconnect
    """
    def __init__(self, host, port, vhost, user, passwd):
        """
        :param host: string
        :param port: string
        :param vhost: string
        :param user: string
        :param passwd: string
        """
        self.host = host
        self.port = port
        self.vhost = vhost
        self.user = user
        self.passwd = passwd

    def connect(self):
        """
        Create blocking connection in RMQ

        :return: pika.BlockingConnection
        """
        return BlockingConnection(
            parameters=ConnectionParameters(
                host=self.host,
                port=self.port,
                virtual_host=self.vhost,
                credentials=PlainCredentials(
                    username=self.user,
                    password=self.passwd,
                )
            )
        )


class Monitor(object):
    """
    Handles connection to RMQ, test of queues and sending notifications
    """
    def __init__(
        self, connector, queue_details, interval=None, max_connections=None
    ):
        """
        :param connector: amqpeek.monitor.Connector
        :param queue_details: dict
        :param interval: float
        :param max_connections: int
        """
        self.connector = connector
        self.queue_details = queue_details
        self.interval = interval
        self.max_connections = max_connections
        self.connection_count = 0
        self.notifiers = []

    def add_notifier(self, notifier):
        """
        :param notifier: amqpeek.notifier.Notifier
        """
        self.notifiers.append(notifier)

    def run(self):
        """
        Main execution loop
        """
        while True:
            try:
                connection = self.connector.connect()
            except AMQPConnectionError:
                subject = 'Connection Error'
                message = 'Error connecting to host: "{host}"'.format(
                    host=self.connector.host
                )

                logging.info('%s - %s', subject, message)
                self.notify(subject, message)
            else:
                self.check_queues(connection, self.queue_details)
                connection.close()

            if self.interval is not None:
                time.sleep(self.interval * 60)
                self.connection_count += 1

                if self.connection_count == self.max_connections:
                    return
            else:
                return

    def check_queues(self, connection, queue_details):
        """
        Check number of messages in queues are within limits

        :param connection: pika.BlockingConnection
        :param queue_details:
        """
        channel = self.get_channel(connection)

        for queue_name, queue_config in queue_details.items():
            queue = self.connect_to_queue(channel, queue_name, queue_config)
            message_count = self.get_queue_message_count(queue)

            if message_count > queue_config['limit']:
                subject = 'Queue Length Error'
                message = (
                    'Queue "{queue}" is over specified limit!! '
                    '({message_count} > {limit})'
                ).format(
                    queue=queue_name,
                    message_count=message_count,
                    limit=queue_config['limit']
                )

                logging.info('%s - %s', subject, message)
                self.notify(subject, message)

    def notify(self, subject, message):
        """
        :param subject: string
        :param message: string
        """
        for notifier in self.notifiers:
            notifier.notify(subject, message)

    def connect_to_queue(self, channel, queue_name, queue_config):
        """
        :param: channel: pika.channel.Channel
        :param: queue_name: string
        :param: queue_config: dict
        :return: pika.frame.Method
        """
        return channel.queue_declare(
            queue=queue_name,
            **queue_config['settings']
        )

    def get_channel(self, connection):
        """
        :param: connection: pika.BlockingConnection
        :return: pika.channel.Channel
        """
        return connection.channel()

    def get_queue_message_count(self, queue):
        """
        :param: queue: pika.frame.Method
        :return: int
        """
        return queue.method.message_count  # pragma: no cover
