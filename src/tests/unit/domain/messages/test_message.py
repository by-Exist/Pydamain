from dataclasses import FrozenInstanceError
import pytest

from pydamain.domain.messages.message import Message, MessageCatchContext
from pydamain.domain.messages import issue


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
        issue(m1)
        issue(m2)
        issue(m2)
    assert {m1, m2} == message_catcher.messages


def test_hook_without_catcher_raise_exception():
    m = ExampleMessage(name="any")
    with pytest.raises(LookupError):
        issue(m)
