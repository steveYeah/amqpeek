#!/usr/bin/env python
from codecs import open
import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), 'r', 'utf-8') as handle:
    readme = handle.read()

config_path = '{}/.amqpeek/'.format(os.path.expanduser("~"))

setup(
    name='amqpeek',
    description='RMQ CLI Monitor',
    packages=find_packages(exclude=['test', 'test.*']),
    version='0.0.1',
    long_description=readme,
    license="MIT",
    author='Steve Hutchins',
    author_email='hutchinsteve@gmail.com',
    url='https://github.com/steveYeah/AmqPeek',
    download_url='https://github.com/steveYeah/amqpeek/archive/v0.0.1.tar.gz',
    keywords=(
        'amqp',
        'monitor',
        'rabbitmq',
        'rabbit',
        'notifier',
        'notifications'
    ),
    data_files=(
        [(config_path, ['config/amqpeek.yaml'])]
    ),
    install_requires=[
        'click',
        'PyYAML',
        'pika',
        'slacker',
    ],
    extras_require={
        'dev': [
            "pep8",
            "pytest",
            "mock",
        ],
    },
    entry_points={
        'console_scripts': [
            'amqpeek=amqpeek.cli:main',
        ],
    }
)
