"""
CLI script and main entry point for amqpeek
"""
import logging
import os
import sys
from shutil import copyfile

import click
import yaml

from .notifier import create_notifiers
from .monitor import Connector, Monitor

DEFAULT_CONFIG = '{}/.amqpeek/amqpeek.yaml'.format(os.path.expanduser("~"))


def gen_config_file():
    dest_path = config_path = '{}/.amqpeek'.format(os.path.expanduser("~"))
    config_file_name = 'amqpeek.yaml'

    full_dest_path = '{0}/{1}'.format(dest_path, config_file_name)

    if not os.path.exists(full_dest_path):
        if not os.path.exists(dest_path):
            os.mkdir(dest_path)

        this_file = os.path.dirname(os.path.realpath(__file__))
        config_file = '{0}/../config/amqpeek.yaml'.format(this_file)
        copyfile(config_file, full_dest_path)

        click.echo(
            click.style(
                'AMQPeek config created in "{}"'.format(full_dest_path),
                fg='green'
            )
        )

        click.echo(
            click.style(
                'Edit file with your details and settings '
                'before running AMQPeek',
                fg='green'
            )
        )
    else:
        click.echo(
            click.style(
                'AMQPeek config already exists in {}'.format(full_dest_path),
                fg='red'
            )
        )


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
@click.option(
    '--gen_config',
    '-g',
    is_flag=True,
    help='Create a empty config file and place it in you current location'
)
def main(config, interval, verbosity, max_tests, gen_config):
    """
    AMQPeek - Simple, flexible RMQ monitor
    """
    configure_logging(verbosity)

    if gen_config:
        gen_config_file()
        sys.exit(0)

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
