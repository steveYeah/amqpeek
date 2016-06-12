"""
CLI script and main entry point for amqpeek
"""
import logging

import click
import yaml

from notifier import create_notifiers
from monitor import Connector, Monitor

DEFAULT_CONFIG = 'etc/rabeye-config.yaml'


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
    default=None,
    help='increase verbosity',
    count=True
)
def main(config, interval, verbosity):
    """
    RabEye - Simple RMQ monitor
    """
    configure_logging(verbosity)
    app_config = read_config(config)

    connector = Connector(**app_config['rabbit_connection'])

    monitor = Monitor(
        connector=connector,
        queue_details=app_config['queues'],
        interval=interval
    )

    notifiers = create_notifiers(app_config['notifiers'])

    for notifier in notifiers:
        monitor.add_notifier(notifier)

    monitor.run()


if __name__ == '__main__':
    main()
