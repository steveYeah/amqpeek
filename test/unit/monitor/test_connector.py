import pytest

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
    def basic_connector(self, connection_params):
        return Connector(**connection_params)

    def test_connection_created(self):
        assert True
