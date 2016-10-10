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
        'click>=6.6',
        'PyYAML>=3.12',
        'pika>=0.10.0',
        'slacker>=0.9.25',
    ],
    extras_require={
        'dev': [
            "pep8>=1.7.0",
            "pytest==3.0.3",
            "mock==2.0.0",
        ],
    },
    entry_points={
        'console_scripts': [
            'amqpeek=amqpeek.cli:main',
        ],
    },
    classifiers=[
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Systems Administration',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
