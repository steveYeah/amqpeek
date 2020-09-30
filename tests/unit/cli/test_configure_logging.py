"""Tests for the logging configuration."""

import logging
from unittest.mock import patch

from amqpeek.cli import configure_logging


class TestConfigureLogging(object):
    """Tests for the config logging method."""

    @patch("amqpeek.cli.logging")
    def test_verbosity_zero_is_error_logging_level(self, logging_patch):
        """Test default logging level is INFO."""
        configure_logging(0)

        assert logging_patch.basicConfig.called_with(
            format="%(message)s", level=logging.INFO
        )

    @patch("amqpeek.cli.logging")
    def test_verbosity_gt_zero_is_info_logging_level(self, logging_patch):
        """Test high verbosity logging is ERROR."""
        configure_logging(1)

        assert logging_patch.basicConfig.called_with(
            format="%(message)s", level=logging.ERROR
        )
