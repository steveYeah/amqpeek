import pytest
from mock import patch

from amqpeek.notifier import create_notifiers, SmtpNotifier, SlackNotifier


class TestNotifierFactory(object):

    @pytest.fixture
    def notifier_data(self):
        return {
            'smtp': {
                'host': '192.168.99.100',
                'user': None,
                'passwd': None,
                'from_addr': 'bob@test.com',
                'to_addr': ['bob@test.com'],
                'subject': 'RabEye - RMQ Monitor',
            },
            'slack': {
                'api_key': 'api_key',
                'username': 'ampeek',
                'channel': '#general',
            },
        }

    def test_create_notifiers_returns_correct_notifiers(
        self, notifier_data
    ):
        # We have to patch SMTP as a connection is established on
        # instantiation
        with patch('amqpeek.notifier.SMTP'):
            notifiers = create_notifiers(notifier_data)

        assert len(notifiers) == len(notifier_data)
        assert isinstance(notifiers[0], SmtpNotifier)
        assert isinstance(notifiers[1], SlackNotifier)
