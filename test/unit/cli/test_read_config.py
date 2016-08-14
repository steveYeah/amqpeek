import pytest

from amqpeek import cli


class TestReadConfig(object):

    test_config_name = 'test_config.yaml'

    @pytest.mark.usefixtures('config_file')
    def test_read_config_returns_correct_data(self, config_data):
        result = cli.read_config(self.test_config_name)

        assert result == config_data

    def test_read_config_file_not_found(self):
        with pytest.raises(IOError):
            cli.read_config('non_existent_file')
