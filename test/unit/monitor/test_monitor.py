import pytest
from mock import Mock
from pika.exceptions import AMQPConnectionError

from amqpeek.monitor import Monitor
from amqpeek.notifier import Notifier


class TestMonitor(object):

    @pytest.fixture
    def monitor(self):
        monitor = Monitor(
            connector=Mock(),
            queue_details={
                'test_queue_1': {
                    'settings': {'durable': True},
                    'limit': 100
                }
            },
            interval=None
        )

        monitor.notifiers = [Mock()]

        return monitor

    def test_add_notifier(self, monitor):
        notifier = Notifier()
        monitor.add_notifier(notifier)

        assert len(monitor.notifiers) == 2
        assert monitor.notifiers[-1] == notifier

    def test_run_failure_to_connect_sends_correct_notification(self, monitor):
        monitor.connector.connect = Mock(side_effect=AMQPConnectionError)
        monitor.connector.host = 'localhost'

        monitor.run()

        monitor.notifiers[0].notify.assert_called_once_with(
            'Connection Error',
            'Error connecting to host: "localhost"'
        )

    def test_run_connects_to_queues(self, monitor):
        channel_mock = Mock()
        monitor.get_channel = Mock(return_value=channel_mock)
        monitor.get_queue_message_count = Mock(return_value=1)

        monitor.run()

        channel_mock.queue_declare.assert_called_once_with(
            queue='test_queue_1',
            durable=True
        )

    def test_run_no_errors_found_do_not_notify(self, monitor):
        monitor.get_queue_message_count = Mock(return_value=1)

        monitor.run()

        monitor.notifiers[0].notify.assert_not_called()

    def test_run_queue_length_error_sends_correct_notification(self, monitor):
        monitor.get_queue_message_count = Mock(return_value=101)

        monitor.run()

        monitor.notifiers[0].notify.assert_called_once_with(
            'Queue Length Error',
            'Queue "test_queue_1" is over specified limit!! (101 > 100)'
        )
