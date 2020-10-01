[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/C0C826VYD)

![Tests](https://github.com/steveYeah/amqpeek/workflows/Tests/badge.svg)
![Coverage](https://github.com/steveYeah/amqpeek/workflows/Coverage/badge.svg)
![Release Drafter](https://github.com/steveYeah/amqpeek/workflows/Release%20Drafter/badge.svg)
![TestPyPi](https://github.com/steveYeah/amqpeek/workflows/TestPyPi/badge.svg)
![Release](https://github.com/steveYeah/amqpeek/workflows/Release/badge.svg)

[![Codecov](https://codecov.io/gh/steveYeah/amqpeek/branch/master/graph/badge.svg)](https://codecov.io/gh/steveYeah/amqpeek)
[![PyPI](https://img.shields.io/pypi/v/amqpeek.svg)](https://pypi.org/project/amqpeek/)

AMQPeek
=======

> A flexible RMQ monitor that keeps track of RMQ, notifying you over
> multiple channels when connections cannot be made, queues have not
> been declared, and when queue lengths increase beyond specified
> limits.

Support OSS, and me :)
----------------------

If you find this project useful, please feel free to [buy me a coffee](https://ko-fi.com/steveyeah)

Install
-------

``` {.sourceCode .shell}
$ pip install amqpeek
```

Once installed, you can then setup AMQPeek to suit your needs by editing
the configuration file

Create configuration file
-------------------------

To create a base configuration file:

``` {.sourceCode .shell}
$ amqpeek --gen_config
```

This will create a file called `amqpeek.yaml` in your current directory.
Here you can setup your connection details for RMQ, define queues you
wish to monitor and define the notifier channels you wish to use. Edit
this file to suit your needs

Running
-------

listing all options:

``` {.sourceCode .shell}
$ amqpeek --help
```

Run AMQPeek with no arguments: This runs the monitoring script once and
then exits out (useful when running AMQPeek as a Cron job)

``` {.sourceCode .shell}
$ amqpeek
```

Run AMQPeek with an interval: This monitors RMQ, running the tests every
10 minutes in a continuous loop (useful when running AMQPeek under
Supervisor or something similar)

``` {.sourceCode .shell}
$ amqpeek --interval 10
```

You can also specify the location of a configuration file to use instead
of the default location of your current directory

``` {.sourceCode .shell}
$ amqpeek --config config.yaml
```

Notification channels
---------------------

AMQPeek supports multiple notification channels.

Currently supported channels:

-   Slack
-   Email (SMTP)

These are controlled via the configuration file, under notifiers. You
can mix and match the notifiers you wish to use, and you can have
multiples of the same notifier types.
