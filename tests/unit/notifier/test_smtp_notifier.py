"""Tests for the notifier module."""

from unittest.mock import patch

import pytest

from amqpeek.notifier import SmtpNotifier


class TestSmtpNotifier(object):
    """Tests for the SmtpNotifier class."""

    @pytest.fixture
    def smtp_notifier_args(self) -> dict:
        """SMTP server args."""
        return {
            "host": "localhost",
            "to_addr": ["test_to@test.com"],
            "from_addr": "test_from@test.com",
            "subject": "Test Subject",
            "user": "user",
            "passwd": "passwd",
        }

    @pytest.fixture
    def smtp_notifier(self, smtp_notifier_args: dict) -> SmtpNotifier:
        """Patch the SmtpNotifier."""
        with patch("amqpeek.notifier.SMTP"):
            return SmtpNotifier(**smtp_notifier_args)

    @pytest.fixture
    def mail_message(self, smtp_notifier_args: dict, message_args: dict) -> str:
        """A mail message for use in tests."""
        return SmtpNotifier.MAIL_TEMPLATE.format(
            from_addr=smtp_notifier_args["from_addr"],
            to_addr=", ".join(smtp_notifier_args["to_addr"]),
            subject="{} - {}".format(
                smtp_notifier_args["subject"], message_args["subject"]
            ),
            message=message_args["message"],
        )

    def test_smtp_login_called_when_credentials_present(
        self, smtp_notifier: SmtpNotifier, smtp_notifier_args: dict
    ) -> None:
        """Test Notifier logs in into SMTP server correctly."""
        smtp_notifier.server.login.assert_called_once_with(
            smtp_notifier_args["user"], smtp_notifier_args["passwd"]
        )

    def test_smtp_login_not_called_when_credentials_not_present(
        self, smtp_notifier_args: dict
    ) -> None:
        """Test SMTP login does not occur if not creds provided."""
        del smtp_notifier_args["user"]
        del smtp_notifier_args["passwd"]

        with patch("amqpeek.notifier.SMTP"):
            smtp_notifier = SmtpNotifier(**smtp_notifier_args)

        smtp_notifier.server.login.assert_not_called()

    def test_notify(self, smtp_notifier: SmtpNotifier, mail_message: str) -> None:
        """Test notify method calls the SMTP server."""
        smtp_notifier.notify(subject="Test message", message="This is a test message")

        smtp_notifier.server.sendmail.assert_called_once_with(
            "test_from@test.com", ["test_to@test.com"], mail_message
        )
