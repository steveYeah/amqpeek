"""
CLI script and main entry point for amqpeek
"""
import logging
import os

import click
import yaml

from .notifier import create_notifiers
from .monitor import Connector, Monitor

DEFAULT_CONFIG = '{}/.amqpeek/'.format(os.path.expanduser("~"))


def read_config(config):
    """
    :param config: string
    :return: dict
    """
    with open(config, 'r') as config_file:
        return yaml.load(config_file)


def configure_logging(verbosity):
    """
    :param verbosity: int
    """
    if verbosity > 0:
        logging.basicConfig(format="%(message)s", level=logging.INFO)
    else:
        logging.basicConfig(format="%(message)s", level=logging.ERROR)


@click.command()
@click.option(
    '--config',
    '-c',
    default=DEFAULT_CONFIG,
    help='Time interval between tests (minutes)'
)
@click.option(
    '--interval',
    '-i',
    type=float,
    default=None,
    help='Time interval between tests (minutes)'
)
@click.option(
    '--verbosity',
    '-v',
    count=True,
    default=0,
    help='increase verbosity'
)
@click.option(
    '--max_tests',
    '-m',
    type=int,
    default=None,
    help='maximum number of tests to run before stopping'
)
def main(config, interval, verbosity, max_tests):
    """
    AMQPeek - Simple, flexible RMQ monitor
    """
    configure_logging(verbosity)
    app_config = read_config(config)

    connector = Connector(**app_config['rabbit_connection'])

    monitor = Monitor(
        connector=connector,
        queue_details=app_config['queues'],
        interval=interval,
        max_connections=max_tests
    )

    notifiers = create_notifiers(app_config['notifiers'])

    for notifier in notifiers:
        monitor.add_notifier(notifier)

    monitor.run()
