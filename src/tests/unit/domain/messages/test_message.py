from dataclasses import FrozenInstanceError
import pytest

from pydamain.domain.messages.message import Message, MessageCatchContext


class ExampleMessage(Message):
    name: str


def test_frozen():
    evt = ExampleMessage(name="foo")
    with pytest.raises(FrozenInstanceError):
        evt.name = "bar"


def test_hook():
    m1 = ExampleMessage(name="foo")
    m2 = ExampleMessage(name="bar")
    with MessageCatchContext() as message_catcher:
        m1.issue_()
        m2.issue_()
        m2.issue_()
    assert {m1, m2} == message_catcher.messages


def test_hook_without_catcher_raise_exception():
    m = ExampleMessage(name="any")
    with pytest.raises(LookupError):
        m.issue_()
