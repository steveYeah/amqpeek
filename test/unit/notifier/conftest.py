import pytest


@pytest.fixture
def message_args():
    return {"subject": "Test message", "message": "This is a test message"}
