"""Tests for the CLI entry point."""

from unittest.mock import Mock, patch

import pytest
from amqpeek.cli import main
from amqpeek.monitor import Connector, Monitor
from click.testing import CliRunner
from pika.exceptions import AMQPConnectionError


class TestCli(object):
    """Tests for the Cli module."""

    @pytest.yield_fixture
    def connector_patch(self):
        """Mocked connector."""
        with patch.object(Connector, "connect") as conn:
            yield conn

    @pytest.yield_fixture
    def queue_count_patch(self):
        """Patched the queue_count method on Monitor."""
        with patch.object(
            Monitor, "get_queue_message_count", return_value=0
        ) as queue_count:
            yield queue_count

    @pytest.yield_fixture
    def mock_notifiers(self):
        """Create mock notifiers."""
        with patch("amqpeek.cli.create_notifiers") as create_notifiers_mock:
            mock_notifiers = (Mock(), Mock())
            create_notifiers_mock.return_value = mock_notifiers

            yield mock_notifiers

    @pytest.fixture
    def cli_runner(self):
        """Creates CLiRunner for use in other tests."""
        return CliRunner()

    @pytest.mark.usefixtures("connector_patch", "queue_count_patch")
    def test_cli_all_ok_no_notify(self, mock_notifiers, cli_runner, config_file):
        """When no queues are over the specified limits, the monitor does not notify."""
        result = cli_runner.invoke(main, ["-c{}".format(config_file)])

        assert result.exit_code == 0
        mock_notifiers[0].notify.assert_not_called()
        mock_notifiers[1].notify.assert_not_called()

    @pytest.mark.usefixtures("connector_patch")
    def test_cli_notify_on_queue_length(
        self, mock_notifiers, queue_count_patch, cli_runner, config_file
    ):
        """When queue is over specified length, notifications sent by all notifiers."""
        queue_count_patch.return_value = 1
        result = cli_runner.invoke(main, ["-c{}".format(config_file)])

        assert result.exit_code == 0
        mock_notifiers[0].notify.assert_called_once_with(
            "Queue Length Error", 'Queue "my_queue" is over specified limit!! (1 > 0)'
        )
        mock_notifiers[0].notify.assert_called_once_with(
            "Queue Length Error", 'Queue "my_queue" is over specified limit!! (1 > 0)'
        )

    def test_cli_notify_on_connection(
        self,
        mock_notifiers,
        queue_count_patch,
        config_data,
        cli_runner,
        config_file,
        connector_patch,
    ):
        """Notifications sent via all notifiers when monitor cannot connect to queue."""
        queue_count_patch.return_value = 1
        connector_patch.side_effect = AMQPConnectionError

        result = cli_runner.invoke(main, ["-c{}".format(config_file)])

        assert result.exit_code == 0

        mock_notifiers[0].notify.assert_called_once_with(
            "Connection Error",
            'Error connecting to host: "{}"'.format(
                config_data["rabbit_connection"]["host"]
            ),
        )
        mock_notifiers[1].notify.assert_called_once_with(
            "Connection Error",
            'Error connecting to host: "{}"'.format(
                config_data["rabbit_connection"]["host"]
            ),
        )

    @patch("amqpeek.monitor.time")
    @pytest.mark.usefixtures("connector_patch", "mock_notifiers", "queue_count_patch")
    def test_cli_wait_and_max_connects(self, time_mock, cli_runner, config_file):
        """Test the wait times and number of connections params are respected."""
        result = cli_runner.invoke(main, ["-c{}".format(config_file), "-i1", "-m1"])

        assert result.exit_code == 0
        time_mock.sleep.assert_called_once_with(1 * 60)

    @patch("amqpeek.cli.open")
    def test_cli_no_config(self, open_patch, mock_notifiers, cli_runner, config_file):
        """Test error is raised and program exits when no config file availiable."""
        open_patch.side_effect = IOError
        result = cli_runner.invoke(main)

        assert result.exit_code == 0
        assert result.output == (
            "No configuration file found. "
            "Specify a configuration file with --config. "
            "To generate a base config file use --gen_config.\n"
        )

    def test_create_config(self, mock_notifiers, cli_runner, config_file):
        """Test a config file can be created."""
        with cli_runner.isolated_filesystem():
            result = cli_runner.invoke(main, ["-g"])

        assert result.exit_code == 0
        assert result.output == (
            "AMQPeek config created\n"
            "Edit the file with your details and settings before running "
            "AMQPeek\n"
        )

    def test_create_config_file_exists(self, mock_notifiers, cli_runner, config_file):
        """Error and exist when attempt to create a config file when one exists."""
        with cli_runner.isolated_filesystem():
            with open("amqpeek.yaml", "w") as f:
                f.write("Some config")
            result = cli_runner.invoke(main, ["-g"])

        assert result.exit_code == 0
        assert result.output == (
            "An AMQPeek config already exists in the current directory\n"
        )
