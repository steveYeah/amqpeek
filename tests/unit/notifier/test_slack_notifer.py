"""Tests the slack notifier module."""

from unittest.mock import patch

import pytest

from amqpeek.notifier import SlackNotifier


class TestSlackNotifier(object):
    """Tests for the SlackNotifier class."""

    @pytest.fixture
    def slack_notifier_args(self) -> dict:
        """Some default args to use for these tests."""
        return {"api_key": "my_key", "username": "test", "channel": "#general"}

    @pytest.fixture
    def slack_notifier(self, slack_notifier_args: dict) -> SlackNotifier:
        """Patch the slack notifier."""
        with patch("amqpeek.notifier.Slacker"):
            return SlackNotifier(**slack_notifier_args)

    def test_notify(
        self,
        slack_notifier: SlackNotifier,
        slack_notifier_args: dict,
        message_args: dict,
    ) -> None:
        """Test the notfiy method calls slack correctly."""
        slack_notifier.notify(
            subject=message_args["subject"], message=message_args["message"]
        )

        slack_notifier.slack.chat.post_message.assert_called_once_with(
            channel=slack_notifier_args["channel"],
            text="{}: {}".format(message_args["subject"], message_args["message"]),
            username=slack_notifier_args["username"],
        )
