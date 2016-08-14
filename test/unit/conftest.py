import os

import pytest
import yaml


@pytest.fixture
def config_data():
    return {
        'rabbit_connection': {
            'user': 'guest',
            'passwd': 'guest',
            'host': '192.168.99.100',
            'port': 5672,
            'vhost': '/',
        },
        'queues': {
            'my_queue': {
                'settings': {'durable': True},
                'limit': 0
            }
        },
        'notifiers': {
            'smtp': {
                'host': '192.168.99.100',
                'user': None,
                'passwd': None,
                'from_addr': 'hutchinsteve@gmail.com',
                'to_addr': ['hutchinsteve@gmail.com'],
                'subject': 'RabEye - RMQ Monitor'
            },
            'slack': {
                'api_key': 'apikey',
                'username': 'ampeek',
                'channel': '#general'
            }
        }
    }


@pytest.yield_fixture
def config_file(config_data):
    test_config_name = 'test_config.yaml'

    fp = open(test_config_name, 'w')
    fp.write(yaml.dump(config_data, default_flow_style=False))
    fp.close()

    yield

    os.remove(test_config_name)
