"""Tests for the creation of notifiers."""

from collections import OrderedDict
from unittest.mock import patch

import pytest
from amqpeek.notifier import create_notifiers, SlackNotifier, SmtpNotifier


class TestNotifierFactory(object):
    """Tests for the notifier factory."""

    @pytest.fixture
    def notifier_data(self):
        """Mock notifier config."""
        data = {
            "smtp": {
                "host": "192.168.99.100",
                "user": None,
                "passwd": None,
                "from_addr": "bob@test.com",
                "to_addr": ["bob@test.com"],
                "subject": "AmqPeek - RMQ Monitor",
            },
            "slack": {
                "api_key": "api_key",
                "username": "ampeek",
                "channel": "#general",
            },
        }
        ordered_data = OrderedDict(sorted(data.items(), key=lambda item: item[0]))

        return ordered_data

    def test_create_notifiers_returns_correct_notifiers(self, notifier_data):
        """Test the correct notifier objects are returned for the given config."""
        # We have to patch SMTP as a connection is established on
        # instantiation
        with patch("amqpeek.notifier.SMTP"):
            notifiers = create_notifiers(notifier_data)

        assert len(notifiers) == len(notifier_data)
        assert isinstance(notifiers[0], SlackNotifier)
        assert isinstance(notifiers[1], SmtpNotifier)

    def tests_create_notifiers_with_no_data_returns_empty_tuple(self):
        """Test create norifiers with empty config."""
        notifiers = create_notifiers({})

        assert len(notifiers) == 0
