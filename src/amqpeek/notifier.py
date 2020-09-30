"""Classes for connecting to different channels to send notifications."""
from smtplib import SMTP

from slacker import Slacker


def create_notifiers(notifier_data):
    """Create the notifiers specificed in the given map.

    Args:
        notifier_data: Map of the required notifiers

    Returns:
        A collection of notifier objects
    """
    if not notifier_data:
        return tuple()

    return tuple(
        NOTIFIER_MAP[notifier_type](**kwargs)
        for notifier_type, kwargs in notifier_data.items()
    )


class Notifier(object):
    """Base Notifier class."""

    def notify(self, subject, message):
        """Send notifications.

        Args:
            subject: The subject of the notification
            message: The body of the notification
        """
        pass  # pragma: no cover


class SmtpNotifier(Notifier):
    """Sends Notifications via SMTP."""

    MAIL_TEMPLATE = """\
    From: {from_addr}
    To: {to_addr}
    Subject: {subject}

    {message}
    """

    def __init__(self, host, to_addr, from_addr, subject, user=None, passwd=None):
        """Creates an SMTP notifier with the given parameters.

        Args:
            host: The host of the SMTP server
            user: The username to use when conencting to the server
            passwd: The password to use to connect to the server
            to_addr: The address to send the emails to
            from_addr: The from address of the emails sent from this notifier
            subject: The subject of the emails
        """
        self.host = host
        self.to_addr = to_addr
        self.from_addr = from_addr
        self.subject = subject
        self.user = user
        self.passwd = passwd
        self.server = SMTP(self.host)

        if self.user is not None:
            self.server.login(self.user, self.passwd)

    def notify(self, subject, message):
        """Send notification via email.

        Args:
            subject: The subject of the email
            message: The body of the email
        """
        subject = "{base_subject} - {subject}".format(
            base_subject=self.subject, subject=subject
        )

        mail_message = self.MAIL_TEMPLATE.format(
            from_addr=self.from_addr,
            to_addr=", ".join(self.to_addr),
            subject=subject,
            message=message,
        )

        self.server.sendmail(self.from_addr, self.to_addr, mail_message)


class SlackNotifier(Notifier):
    """Send notifications via Slack."""

    def __init__(self, api_key, username, channel):
        """Create a Slack notifier with the given parameters.

        Args:
            api_key: The API key used to connect to Slack
            username: The username of the message sender on Slack
            channel: The channel to send the message to
        """
        self.username = username
        self.channel = channel
        self.slack = Slacker(api_key)

    def notify(self, subject, message):
        """Send notification via Slack.

        Args:
            subject: The subject of the message
            message: The message body
        """
        message = "{subject}: {message}".format(subject=subject, message=message)

        self.slack.chat.post_message(
            channel=self.channel, text=message, username=self.username
        )


NOTIFIER_MAP = {"smtp": SmtpNotifier, "slack": SlackNotifier}
