"""Fixtures shared in the notifier tests."""
from typing import Dict

import pytest


@pytest.fixture
def message_args() -> Dict[str, str]:
    """A formatted message."""
    return {"subject": "Test message", "message": "This is a test message"}
