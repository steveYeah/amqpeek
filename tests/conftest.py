"""Fixtures availiable to the entire suite."""
import os

import pytest
import yaml


@pytest.fixture
def config_data() -> dict:
    """Dummy config data."""
    return {
        "rabbit_connection": {
            "user": "guest",
            "passwd": "guest",
            "host": "localhost",
            "port": 5672,
            "vhost": "/",
        },
        "queues": {"my_queue": {"settings": {"durable": True}, "limit": 0}},
        "queue_limits": {0: ["my_queue"], 1: ["my_other_queue"]},
        "notifiers": {
            "smtp": {
                "host": "localhost",
                "user": None,
                "passwd": None,
                "from_addr": "test@test.com",
                "to_addr": ["test@yourtest.com"],
                "subject": "AMQPeek - RMQ Monitor",
            },
            "slack": {"api_key": "apikey", "username": "ampeek", "channel": "#general"},
        },
    }


@pytest.yield_fixture
def config_file(config_data: dict) -> str:
    """Creates a temporary config file used by the tests."""
    # TODO: Use the tempfile module
    test_config_name = "test_config.yaml"

    fp = open(test_config_name, "w")
    fp.write(yaml.dump(config_data, default_flow_style=False))
    fp.close()

    yield test_config_name

    os.remove(test_config_name)
