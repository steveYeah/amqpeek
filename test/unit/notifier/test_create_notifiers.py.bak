import pytest
from collections import OrderedDict
from mock import patch

from amqpeek.notifier import create_notifiers, SmtpNotifier, SlackNotifier


class TestNotifierFactory(object):

    @pytest.fixture
    def notifier_data(self):
        data = {
            'smtp': {
                'host': '192.168.99.100',
                'user': None,
                'passwd': None,
                'from_addr': 'bob@test.com',
                'to_addr': ['bob@test.com'],
                'subject': 'AmqPeek - RMQ Monitor',
            },
            'slack': {
                'api_key': 'api_key',
                'username': 'ampeek',
                'channel': '#general',
            },
        }
        ordered_data = OrderedDict(
            sorted(data.items(), key=lambda item: item[0])
        )

        return ordered_data

    def test_create_notifiers_returns_correct_notifiers(
        self, notifier_data
    ):
        # We have to patch SMTP as a connection is established on
        # instantiation
        with patch('amqpeek.notifier.SMTP'):
            notifiers = create_notifiers(notifier_data)

        assert len(notifiers) == len(notifier_data)
        assert isinstance(notifiers[0], SlackNotifier)
        assert isinstance(notifiers[1], SmtpNotifier)
