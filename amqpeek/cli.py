"""
CLI script and main entry point for amqpeek
"""
import logging
import os
import sys
from shutil import copyfile

import click
import yaml

from .exceptions import ConfigExistsError
from .notifier import create_notifiers
from .monitor import Connector, Monitor

DEFAULT_CONFIG = 'amqpeek.yaml'


def gen_config_file():
    if os.path.exists(DEFAULT_CONFIG):
        raise ConfigExistsError('File already exists')

    this_file = os.path.dirname(os.path.realpath(__file__))
    config_file = '{0}/../config/amqpeek.yaml'.format(this_file)
    copyfile(config_file, DEFAULT_CONFIG)


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


def build_queue_data(app_config):
    queue_config = []
    config_queues = app_config.get('queues')
    queue_limits = app_config.get('queue_limits')

    if config_queues:
        for queue_name, dets in config_queues.items():
            queue_config.append((queue_name, dets['limit']))

    if queue_limits:
        for limit, queues in queue_limits.items():
            for queue_name in queues:
                queue_config.append((queue_name, limit))

    return set(queue_config)


@click.command()
@click.option(
    '--config',
    '-c',
    default=DEFAULT_CONFIG,
    help=(
        'Location of configuration file to use '
        '(defaults to "amqpeek.yaml" in current directory)'
    )
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
    help='Increase verbosity'
)
@click.option(
    '--max_tests',
    '-m',
    type=int,
    default=None,
    help='Maximum number of tests to run before stopping'
)
@click.option(
    '--gen_config',
    '-g',
    is_flag=True,
    help=(
        'Create a basic configuration file and place it in your '
        'current directory'
    )
)
def main(config, interval, verbosity, max_tests, gen_config):
    """
    AMQPeek - Simple, flexible RMQ monitor
    """
    configure_logging(verbosity)

    if gen_config:
        try:
            gen_config_file()
        except ConfigExistsError:
            click.echo(
                click.style(
                    'An AMQPeek config already exists in the current '
                    'directory',
                    fg='red'
                )
            )
        else:
            click.echo(
                click.style(
                    'AMQPeek config created',
                    fg='green'
                )
            )

            click.echo(
                click.style(
                    'Edit the file with your details and settings '
                    'before running AMQPeek',
                    fg='green'
                )
            )

        sys.exit(0)

    try:
        app_config = read_config(config)
    except IOError:
        click.echo(
            click.style(
                'No configuration file found. '
                'Specify a configuration file with --config. '
                'To generate a base config file use --gen_config.',
                fg='red'
            )
        )

        sys.exit(0)

    connector = Connector(**app_config['rabbit_connection'])

    queue_config = build_queue_data(app_config)

    monitor = Monitor(
        connector=connector,
        queue_details=queue_config,
        interval=interval,
        max_connections=max_tests
    )

    notifiers = create_notifiers(app_config['notifiers'])

    for notifier in notifiers:
        monitor.add_notifier(notifier)

    monitor.run()
