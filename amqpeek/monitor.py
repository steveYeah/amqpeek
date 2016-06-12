"""
Connection and monitoring of RMQ
"""
import logging
import time

import pika
import pika.exceptions


class Connector(object):
    """
    Abstracted connection to RMQ, Holds credentials
    for continued connection drop and reconnect
    """

    def __init__(self, host, port, vhost, user, passwd):
        """
        :param host: string
        :param port: string
        :param vhost: string
        :param user: string
        :param passwd: string
        """
        self.conn_params = {
            'host': host,
            'port': port,
            'virtual_host': vhost,
        }

        if user and passwd:
            self.conn_params['credentials'] = pika.PlainCredentials(
                username=user,
                password=passwd,
            )

    @property
    def host(self):
        """
        :return: string
        """
        return self.conn_params['host']

    def connect(self):
        return pika.BlockingConnection(
            parameters=pika.ConnectionParameters(**self.conn_params)
        )


class Monitor(object):
    """
    Handles connection to RMQ, test of queues and sending notifications
    """

    def __init__(self, connector, queue_details, interval=None):
        """
        :param connector: amqpeek.monitor.Connector
        :param queue_details: dict
        :param interval: float
        """
        self.connector = connector
        self.queue_details = queue_details
        self.interval = interval
        self.notifiers = []

    def add_notifier(self, notifier):
        """
        :param notifier: amqpeek.notifier.Notifier
        """
        self.notifiers.append(notifier)

    def run(self):
        while True:
            try:
                connection = self.connector.connect()
            except pika.exceptions.AMQPConnectionError:
                subject = 'Connection Error'
                message = 'Error connecting to host: "{host}"'.format(
                    host=self.connector.host
                )

                logging.info('%s - %s', subject, message)
                self.notify(subject, message)
            else:
                self.check_queues(connection, self.queue_details)
                connection.close()

            if self.interval is None:
                return

            time.sleep(self.interval * 60)

    def check_queues(self, connection, queue_details):
        """
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
        return channel.queue_declare(
            queue=queue_name,
            **queue_config['settings']
        )

    def get_channel(self, connection):
        return connection.channel()

    def get_queue_message_count(self, queue):
        return queue.method.message_count
