"""Fixtures shared in the notifier tests."""
import pytest


@pytest.fixture
def message_args():
    """A formatted message."""
    return {"subject": "Test message", "message": "This is a test message"}
