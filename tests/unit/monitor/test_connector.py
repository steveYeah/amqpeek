"""Tests for the Connector module."""

from unittest.mock import MagicMock, Mock, patch

import pytest

from amqpeek.monitor import Connector


class TestConnector(object):
    """Tests for the Connector class."""

    @pytest.fixture
    def connection_params(self) -> dict:
        """Connection params."""
        return {
            "host": "localhost",
            "port": 5672,
            "vhost": "/",
            "user": "guest",
            "passwd": "guest",
        }

    @pytest.fixture
    def connector(self, connection_params: dict) -> Connector:
        """Creates a connector for use in other tests."""
        return Connector(**connection_params)

    @patch("amqpeek.monitor.BlockingConnection")
    @patch("amqpeek.monitor.ConnectionParameters")
    @patch("amqpeek.monitor.PlainCredentials")
    def test_connection_created(
        self,
        plain_credentials: MagicMock,
        connection_params_mock: MagicMock,
        blocking_connection_mock: MagicMock,
        connector: Connector,
        connection_params: dict,
    ) -> None:
        """Test a connection attempt is made with the supplied details."""
        credentials_instance_mock = Mock()
        plain_credentials.return_value = credentials_instance_mock

        connection_params_instance_mock = Mock()
        connection_params_mock.return_value = connection_params_instance_mock

        connector.connect()

        plain_credentials.assert_called_once_with(
            username=connection_params["user"], password=connection_params["passwd"]
        )

        connection_params_mock.assert_called_once_with(
            host=connection_params["host"],
            port=connection_params["port"],
            virtual_host=connection_params["vhost"],
            credentials=credentials_instance_mock,
        )

        blocking_connection_mock.assert_called_once_with(
            parameters=connection_params_instance_mock
        )
