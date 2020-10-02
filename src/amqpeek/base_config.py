"""A Template for the base config."""

DEFAULT_LOCATION = "amqpeek.yaml"

BASE_CONFIG = """
# RMQ connection details
rabbit_connection: {
  user: guest,
  passwd: guest,
  host: localhost,
  port: 5672,
  vhost: /,
}

# Queues to monitor.
#
# Define a queue you wish to monitor and the warning limit of that queue
# An alternative to defining queues is queue_limits below.
#
# limit:
# max items in queue before notification is sent
queues:
  my_queue: {
      'limit': 10
  }

  my_other_queue: {
      'limit': 10
  }

  my_other_other_queue: {
      'limit': 100
  }

# Limits and associated queues.
#
# Define a number of queues grouped by limit.
#
# This is an alternative approach to
# defining queues individually, as shown above.
#
# key:
# max items in queue before notification is sent
#
# value:
# list of queue names to apply the limit to
queue_limits:
  10: ['my_queue', 'my_other_queue']
  100: ['my_other_other_queue']

# Active notifiers:
#
# Currently supported notifers are listed below with example
# settings
notifiers:
  smtp: {
      host: localhost,
      user: ~,
      passwd: ~,
      from_addr: youremail@example.com,
      to_addr: [theiremail@example.com],
      subject: 'AMQPeek - RMQ Monitor'
  }

  slack: {
      api_key: your-api-key,
      username: ampeek,
      channel: '#general'
  }
"""
