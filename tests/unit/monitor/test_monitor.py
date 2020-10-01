"""Tests for the monitor module."""

from unittest.mock import MagicMock, Mock, patch

import pytest
from pika.exceptions import AMQPConnectionError, ChannelClosed

from amqpeek.monitor import Monitor
from amqpeek.notifier import Notifier


class TestMonitor(object):
    """Tests for the monitor class."""

    @pytest.fixture
    def monitor(self) -> Monitor:
        """Creates a monitor with a mocked connector."""
        monitor = Monitor(
            connector=Mock(), queue_details=[("test_queue_1", 100)], interval=None
        )

        monitor.notifiers = [Mock()]

        return monitor

    def test_add_notifier(self, monitor: Monitor) -> None:
        """Test add_notifier adds notifiers correctly."""
        notifier = Notifier()
        monitor.add_notifier(notifier)

        assert len(monitor.notifiers) == 2
        assert monitor.notifiers[-1] == notifier

    def test_run_failure_to_connect_sends_correct_notification(
        self, monitor: Monitor
    ) -> None:
        """Test the correct notifications are send when failing to connect to RMQ."""
        monitor.connector.connect = Mock(side_effect=AMQPConnectionError)
        monitor.connector.host = "localhost"

        monitor.run()

        monitor.notifiers[0].notify.assert_called_once_with(
            "Connection Error", 'Error connecting to host: "localhost"'
        )

    def test_run_connects_to_queues(self, monitor: Monitor) -> None:
        """Test connection works correctly."""
        channel_mock = Mock()
        monitor.get_channel = Mock(return_value=channel_mock)
        monitor.get_queue_message_count = Mock(return_value=1)

        monitor.run()

        monitor.get_queue_message_count.assert_called()
        channel_mock.queue_declare.assert_called_once_with(
            queue="test_queue_1", passive=True
        )

    def test_run_no_errors_found_do_not_notify(self, monitor: Monitor) -> None:
        """Test no notifications are sent when no errors found."""
        monitor.get_queue_message_count = Mock(return_value=1)

        monitor.run()

        monitor.notifiers[0].notify.assert_not_called()

    def test_run_queue_length_error_sends_correct_notification(
        self, monitor: Monitor
    ) -> None:
        """Test correct notification sent when the Q length is exceeded."""
        monitor.get_queue_message_count = Mock(
            # the limit of test_queue_one + 1
            return_value=monitor.queue_details[0][1]
            + 1
        )

        monitor.run()

        monitor.notifiers[0].notify.assert_called_once_with(
            "Queue Length Error",
            'Queue "test_queue_1" is over specified limit!! (101 > 100)',
        )

    def test_run_queue_not_declared_send_correct_notifcation(
        self, monitor: Monitor
    ) -> None:
        """Test correct notifications are sent when the Q is not found."""
        monitor.connect_to_queue = Mock(side_effect=ChannelClosed(404, "NOT FOUND"))

        monitor.run()

        monitor.notifiers[0].notify.assert_called_once_with(
            "Queue does not exist", 'Queue "test_queue_1" has not been declared'
        )

    @patch("amqpeek.monitor.time")
    def test_run_use_interval(self, time_mock: MagicMock, monitor: Monitor) -> None:
        """Test the interval parameter is respected."""
        monitor.interval = 10
        monitor.max_connections = 2
        monitor.get_queue_message_count = Mock(return_value=1)

        monitor.run()

        time_mock.sleep.assert_called_with(monitor.interval * 60)
