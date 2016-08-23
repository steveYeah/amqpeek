.. image:: https://img.shields.io/travis/steveYeah/amqpeek.svg?branch=master
   :target: https://travis-ci.org/steveYeah/amqpeek


AMQPeek
=======

.. pull-quote::

    A flexible RMQ monitor that keeps track of RMQ, notifying you over multiple channels when
    connections cannot be made, and when queue lengths increase beyond specified limits.


**Note: not yet released on PyPI. Coming very soon**

Install
-------
.. code-block:: shell

    $ pip install amqpeek

Once installed, you can then setup AMQPeek to suit your needs by editing the configuration file
located in ``~/.amqpeek/amqpeek.yaml``

Running
-------

listing all options:

.. code-block:: shell

    $ amqpeek --help

Run AMQPeek with no arguments.
This runs the monitoring script once and then exits out (useful when running AMQPeek as a Cron job)

.. code-block:: shell

    $ amqpeek

Run AMQPeek with an interval. This monitors RMQ, running the tests every 10 minutes in a
continues loop (useful when running AMQPeek under Supervisor or something similar)

.. code-block:: shell

    $ amqpeek --interval 10

You can also specify the location of a configuration file to use instead of the default
configuration file located in your home directory

.. code-block:: shell

    $ amqpeek --config config.yaml


Notification channels
---------------------

AMQPeek supports multiple notification channels.

Currently supported channels:

* Slack
* Email (SMTP)

These are controlled via the configuration file, under notifiers. You can mix and match
the notifiers you wish to use, and you can have multiples of the same notifier types.
