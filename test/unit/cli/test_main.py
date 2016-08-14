import pytest
from amqpeek.monitor import Monitor
from click.testing import CliRunner
from mock import patch, Mock, DEFAULT
from pika.exceptions import AMQPConnectionError

from amqpeek.cli import main


class TestCli(object):

    @pytest.yield_fixture
    def rabbit_conn_patch(self):
        with patch('amqpeek.monitor.PlainCredentials'):
            with patch('amqpeek.monitor.ConnectionParameters'):
                with patch('amqpeek.monitor.BlockingConnection'):
                    yield

    @pytest.yield_fixture
    def queue_count_patch(self):
        with patch.object(
            Monitor, 'get_queue_message_count', return_value=0
        ) as queue_count:
            yield queue_count

    @pytest.yield_fixture
    def mock_notifiers(self):
        with patch('amqpeek.cli.create_notifiers') as create_notifiers_mock:
            mock_notifiers = (Mock(), Mock())
            create_notifiers_mock.return_value = mock_notifiers

            yield mock_notifiers

    @pytest.fixture
    def cli_runner(self):
        return CliRunner()

    @pytest.mark.usefixtures(
        'config_file', 'rabbit_conn_patch', 'queue_count_patch'
    )
    def test_cli_all_ok_no_notify(self, mock_notifiers, cli_runner):
        result = cli_runner.invoke(main, ['-ctest_config.yaml'])

        assert result.exit_code == 0
        mock_notifiers[0].notify.assert_not_called()
        mock_notifiers[1].notify.assert_not_called()

    @pytest.mark.usefixtures('config_file', 'rabbit_conn_patch')
    def test_cli_notify_on_queue_length(
        self, mock_notifiers, queue_count_patch, cli_runner
    ):
        queue_count_patch.return_value = 1
        result = cli_runner.invoke(main, ['-ctest_config.yaml'])

        assert result.exit_code == 0
        mock_notifiers[0].notify.assert_called_once_with(
            'Queue Length Error',
            'Queue "my_queue" is over specified limit!! (1 > 0)'
        )
        mock_notifiers[0].notify.assert_called_once_with(
            'Queue Length Error',
            'Queue "my_queue" is over specified limit!! (1 > 0)'
        )

    @pytest.mark.usefixtures('config_file')
    def test_cli_notify_on_connection(
        self, mock_notifiers, queue_count_patch, cli_runner
    ):
        queue_count_patch.return_value = 1

        with patch('amqpeek.monitor.Connector') as connector_mock:
            connector_mock.connect = Mock(side_effect=AMQPConnectionError)

            result = cli_runner.invoke(main, ['-ctest_config.yaml'])

        assert result.exit_code == 0

        mock_notifiers[0].notify.assert_called_once_with(
            'Connection Error',
            'Error connecting to host: "192.168.99.100"'
        )
        mock_notifiers[1].notify.assert_called_once_with(
            'Connection Error',
            'Error connecting to host: "192.168.99.100"'
        )

    @patch('amqpeek.monitor.time')
    @pytest.mark.usefixtures(
        'config_file', 'mock_notifiers', 'queue_count_patch'
    )
    def test_cli_wait_and_max_connects(self, time_mock, cli_runner):
        result = cli_runner.invoke(
            main,
            ['-ctest_config.yaml', '-i1', '-m1']
        )

        assert result.exit_code == 0
        time_mock.sleep.assert_called_once_with(1 * 60)
