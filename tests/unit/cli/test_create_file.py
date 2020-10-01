"""Tests the create config command."""
from unittest.mock import MagicMock, patch

import pytest

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
    @patch("amqpeek.cli.copyfile")
    @patch("amqpeek.cli.os.path.dirname")
    def test_file_created(
        self,
        path_dirname_patch: MagicMock,
        copyfile_patch: MagicMock,
        path_exists_patch: MagicMock,
    ) -> None:
        """Test the file is actually created."""
        path_exists_patch.return_value = False
        this_file = "current_file_location"

        path_dirname_patch.return_value = this_file
        config_file = "{0}/../../config/amqpeek.yaml".format(this_file)

        gen_config_file()

        copyfile_patch.assert_called_once_with(config_file, "amqpeek.yaml")
