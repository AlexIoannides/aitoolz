"""Dummy tests."""
from aitoolz.hello_world import message


def test_message():
    assert message() == "Hello, world!"
