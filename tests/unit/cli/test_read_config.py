"""Tests for reading the config file."""
import pytest

from amqpeek import cli


class TestReadConfig(object):
    """Tests the read_config method on the CLI class."""

    def test_read_config_returns_correct_data(
        self, config_data: dict, config_file: str
    ) -> None:
        """Tests the config is read and returned in the correct format."""
        result = cli.read_config(config_file)

        assert result == config_data

    def test_read_config_file_not_found(self) -> None:
        """Tests the correct exception is raised when the config is not found."""
        with pytest.raises(IOError):
            cli.read_config("non_existent_file")
