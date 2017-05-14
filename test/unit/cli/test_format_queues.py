from copy import deepcopy

from amqpeek.cli import build_queue_data


class TestFormatQueues:
    def test_dedup_queue_config(self, config_data):
        """
        my_queue is defined twice, both in queues and queue_limits
        build_queue_data should dedup queues defined twice if their limits
        are the same
        """
        result = build_queue_data(config_data)

        assert isinstance(result, set)
        assert len(result) == 2

        expected_queues = set([('my_queue', 0), ('my_other_queue', 1)])
        for excepted_queue in expected_queues:
            assert excepted_queue in result

    def test_just_queue_config(self, config_data):
        config_data = deepcopy(config_data)
        del(config_data['queue_limits'])

        result = build_queue_data(config_data)

        assert result == {('my_queue', 0)}

    def test_just_queue_limits_config(self, config_data):
        config_data = deepcopy(config_data)
        del(config_data['queues'])

        result = build_queue_data(config_data)

        assert len(result) == 2

        expected_queues = set([('my_queue', 0), ('my_other_queue', 1)])
        for excepted_queue in expected_queues:
            assert excepted_queue in result

    def test_no_queue_config(self):
        result = build_queue_data({})

        assert result == set([])
