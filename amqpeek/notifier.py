"""
Classes for connecting to different channels to send
notifications
"""
from smtplib import SMTP

from slacker import Slacker


def create_notifiers(notifier_data):
    """
    :param notifier_data: dict
    :return: tuple
    """
    return tuple(
        NOTIFIER_MAP[notifier_type](**kwargs) 
        for notifier_type, kwargs in notifier_data.items()
    )


class Notifier(object):
    """
    Base Notifier class
    """
    def notify(self, subject, message):
        """
        Send notifications
        """
        pass  # pragma: no cover


class SmtpNotifier(Notifier):
    """
    Sends Notifications via SMTP
    """
    MAIL_TEMPLATE = """\
    From: {from_addr}
    To: {to_addr}
    Subject: {subject}

    {message}
    """

    def __init__(
        self, host, to_addr, from_addr, subject, user=None, passwd=None
    ):
        """
        :param host: string
        :param user: string
        :param passwd: string
        :param to_addr: string
        :param from_addr: string
        :param subject: string
        :param user: string
        :param: passwd
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
        """
        :param subject: string
        :param message: string
        """
        subject = "{base_subject} - {subject}".format(
            base_subject=self.subject,
            subject=subject
        )

        mail_message = self.MAIL_TEMPLATE.format(
            from_addr=self.from_addr,
            to_addr=", ".join(self.to_addr),
            subject=subject,
            message=message
        )

        self.server.sendmail(
            self.from_addr,
            self.to_addr,
            mail_message
        )


class SlackNotifier(Notifier):
    """
    Send notifications via Slack
    """
    def __init__(self, api_key, username, channel):
        """
        :param api_key: string
        :param username: string
        :param channel: string
        """
        self.username = username
        self.channel = channel
        self.slack = Slacker(api_key)

    def notify(self, subject, message):
        """
        :param subject: string
        :param message: string
        """
        message = "{subject}: {message}".format(
            subject=subject,
            message=message
        )

        self.slack.chat.post_message(
            channel=self.channel,
            text=message,
            username=self.username
        )


NOTIFIER_MAP = {
    'smtp': SmtpNotifier,
    'slack': SlackNotifier,
}
