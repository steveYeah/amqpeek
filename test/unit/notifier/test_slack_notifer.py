import mock
import pytest

from amqpeek.notifier import SlackNotifier


class TestSlackNotifier(object):

    @pytest.fixture
    def slack_notifier_args(self):
        return {
            'api_key': 'my_key',
            'username': 'test',
            'channel': '#general',
        }

    @pytest.fixture
    def slack_notifier(self, slack_notifier_args):
        with mock.patch('amqpeek.notifier.Slacker'):
            return SlackNotifier(**slack_notifier_args)

    def test_notify(self, slack_notifier, slack_notifier_args, message_args):
        slack_notifier.notify(
            subject=message_args['subject'],
            message=message_args['message']
        )

        slack_notifier.slack.chat.post_message.assert_called_once_with(
            channel=slack_notifier_args['channel'],
            text='{}: {}'.format(
                message_args['subject'],
                message_args['message']
            ),
            username=slack_notifier_args['username']
        )
