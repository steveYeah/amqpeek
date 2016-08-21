import pytest
from mock import Mock, patch

from amqpeek.monitor import Connector


class TestConnector(object):

    @pytest.fixture
    def connection_params(self):
        return {
            'host': 'localhost',
            'port': 5672,
            'vhost': '/',
            'user': 'guest',
            'passwd': 'guest'
        }

    @pytest.fixture
    def connector(self, connection_params):
        return Connector(**connection_params)

    @patch('amqpeek.monitor.BlockingConnection')
    @patch('amqpeek.monitor.ConnectionParameters')
    @patch('amqpeek.monitor.PlainCredentials')
    def test_connection_created(
        self, plain_credentials, connection_params_mock,
        blocking_connection_mock, connector, connection_params
    ):
        credentials_instance_mock = Mock()
        plain_credentials.return_value = credentials_instance_mock

        connection_params_instance_mock = Mock()
        connection_params_mock.return_value = connection_params_instance_mock

        connector.connect()

        plain_credentials.assert_called_once_with(
            username=connection_params['user'],
            password=connection_params['passwd']
        )

        connection_params_mock.assert_called_once_with(
            host=connection_params['host'],
            port=connection_params['port'],
            virtual_host=connection_params['vhost'],
            credentials=credentials_instance_mock
        )

        blocking_connection_mock.assert_called_once_with(
            parameters=connection_params_instance_mock
        )
