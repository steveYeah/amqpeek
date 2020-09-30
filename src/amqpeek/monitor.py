"""Connecting to, and monitoring of RMQ."""
import logging
import time

from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.exceptions import AMQPConnectionError, ChannelClosed


class Connector(object):
    """Abstracted connection to RMQ.

    Holds credentials for continued connection drop and reconnect.
    """

    def __init__(self, host, port, vhost, user, passwd):
        """Create Connector with given config.

        Args:
            host: Host of the RMQ server
            port: Port the RMQ server is running on
            vhost: RMQ vhost
            user: User name used to connection to RMQ server
            passwd: Password used to connect to RMQ server
        """
        self.host = host
        self.port = port
        self.vhost = vhost
        self.user = user
        self.passwd = passwd

    def connect(self):
        """Create blocking connection in RMQ.

        Returns:
            A BlockingConnection to the RMQ server specified
        """
        return BlockingConnection(
            parameters=ConnectionParameters(
                host=self.host,
                port=self.port,
                virtual_host=self.vhost,
                credentials=PlainCredentials(username=self.user, password=self.passwd),
            )
        )


class Monitor(object):
    """Handles connection to RMQ, test of queues and sending notifications."""

    def __init__(self, connector, queue_details, interval=None, max_connections=None):
        """Creates a Monitor with the given parameters.

        Args:
            connector: The connector object used to create a connection to the
                RMQ server to be monitored
            queue_details: The map of the queues to connect to and there limits
            interval: The time to wait between checks
            max_connections: The max time to connect the RMQ server before exiting
        """
        self.connector = connector
        self.queue_details = queue_details
        self.interval = interval
        self.max_connections = max_connections
        self.connection_count = 0
        self.notifiers = []

    def add_notifier(self, notifier):
        """Adds a notifier to this monitor that will be used to send notifications to.

        Args:
            notifier: The notifier to add to the monitor
        """
        self.notifiers.append(notifier)

    def run(self):
        """Main execution loop."""
        while True:
            try:
                connection = self.connector.connect()
            except AMQPConnectionError:
                subject = "Connection Error"
                message = 'Error connecting to host: "{host}"'.format(
                    host=self.connector.host
                )

                logging.info("%s - %s", subject, message)
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
        """Check number of messages in queues are within limits.

        Args:
            connection: The connection object representing the connection to the RMQ server
            queue_details: A map of the queues and thier specified limits
        """
        channel = self.get_channel(connection)

        for queue_name, queue_limit in queue_details:
            try:
                queue = self.connect_to_queue(channel, queue_name)
            except ChannelClosed:
                subject = "Queue does not exist"
                message = ('Queue "{queue}" has not been declared').format(
                    queue=queue_name
                )

                logging.info("%s - %s", subject, message)
                self.notify(subject, message)

                continue

            message_count = self.get_queue_message_count(queue)

            if message_count > queue_limit:
                subject = "Queue Length Error"
                message = (
                    'Queue "{queue}" is over specified limit!! '
                    "({message_count} > {limit})"
                ).format(
                    queue=queue_name, message_count=message_count, limit=queue_limit
                )

                logging.info("%s - %s", subject, message)
                self.notify(subject, message)

    def notify(self, subject, message):
        """Main entry point for sending notifications using this monitors notifiers.

        Args:
            subject: The subject of the notification
            message: The main body of the notification
        """
        for notifier in self.notifiers:
            notifier.notify(subject, message)

    def connect_to_queue(self, channel, queue_name):
        """Connect to the given queue on the given channel.

        Args:
            channel: The active channel to the RMQ server
            queue_name: The queue to connect too

        Returns:
            A representation of the requested queue, holding data about the
            number of messages, amongst other things
        """
        return channel.queue_declare(queue=queue_name, passive=True)

    def get_channel(self, connection):
        """Get the channel from the given connection.

        Args:
            connection: The connection to the RMQ server

        Returns:
            The active channel to the RMQ server
        """
        return connection.channel()

    def get_queue_message_count(self, queue):
        """Get the number of messages on the given queue at time of connection.

        Args:
            queue: The queue we want to get the count of messages from

        Returns:
            The number of messages on the queue at time of connection
        """
        return queue.method.message_count  # pragma: no cover
