import pytest

from amqpeek import cli


class TestReadConfig(object):

    def test_read_config_returns_correct_data(self, config_data, config_file):
        result = cli.read_config(config_file)

        assert result == config_data

    def test_read_config_file_not_found(self):
        with pytest.raises(IOError):
            cli.read_config('non_existent_file')
