import mock
import pytest

from amqpeek.notifier import SmtpNotifier, mail_template


class TestSmtpNotifer(object):

    @pytest.fixture
    def smtp_notifier_args(self):
        return {
            'host': 'localhost',
            'to_addr': ['test_to@test.com'],
            'from_addr': 'test_from@test.com',
            'subject': 'Test Subject',
            'user': 'user',
            'passwd': 'passwd'
        }

    @pytest.fixture
    def smtp_notifier(self, smtp_notifier_args):
        del(smtp_notifier_args['user'])
        del(smtp_notifier_args['passwd'])

        return SmtpNotifier(**smtp_notifier_args)

    @pytest.fixture
    def smtp_notifier_auth(self, smtp_notifier_args):
        return SmtpNotifier(
            **smtp_notifier_args
        )

    @pytest.fixture
    def mail_message(self, smtp_notifier_args, message_args):
        return mail_template.format(
            from_addr=smtp_notifier_args['from_addr'],
            to_addr=", ".join(smtp_notifier_args['to_addr']),
            subject='{} - {}'.format(
                smtp_notifier_args['subject'],
                message_args['subject']
            ),
            message=message_args['message']
        )

    def test_notify(self, smtp_notifier, mail_message):
        with mock.patch('amqpeek.notifier.SMTP'):
            smtp_notifier.notify(
                subject='Test message',
                message='This is a test message'
            )

            smtp_notifier.server.sendmail.assert_called_once_with(
                'test_from@test.com',
                ['test_to@test.com'],
                mail_message
            )

            smtp_notifier.server.login.assert_not_called()

    def test_no_login_on_notify(
        self, smtp_notifier_auth, smtp_notifier_args, mail_message
    ):
        with mock.patch('amqpeek.notifier.SMTP'):
            smtp_notifier_auth.notify(
                subject='Test message',
                message='This is a test message'
            )

            smtp_notifier_auth.server.sendmail.assert_called_once_with(
                'test_from@test.com',
                ['test_to@test.com'],
                mail_message
            )

            smtp_notifier_auth.server.login.assert_called_once_with(
                smtp_notifier_args['user'],
                smtp_notifier_args['passwd']
            )
