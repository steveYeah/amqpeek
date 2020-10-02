"""Tests the create config command."""
from unittest.mock import MagicMock, mock_open, patch

import pytest

from amqpeek.base_config import BASE_CONFIG, DEFAULT_LOCATION
from amqpeek.cli import gen_config_file
from amqpeek.exceptions import ConfigExistsError


class TestGenConfigFile:
    """Tests the gen config command."""

    @patch("amqpeek.cli.os.path.exists")
    def test_file_already_exists(self, path_exists_patch: MagicMock) -> None:
        """Test correct exception is raised then the config file already exists."""
        path_exists_patch.return_value = True

        with pytest.raises(ConfigExistsError):
            gen_config_file()

    @patch("amqpeek.cli.os.path.exists")
    @patch("amqpeek.cli.open", new_callable=mock_open)
    def test_file_created(
        self,
        open_patch: MagicMock,
        path_exists_patch: MagicMock,
    ) -> None:
        """Test the file is actually created."""
        path_exists_patch.return_value = False

        gen_config_file()

        open_patch.assert_called_with(DEFAULT_LOCATION, "w")
        open_patch.return_value.write.assert_called_once_with(BASE_CONFIG)
