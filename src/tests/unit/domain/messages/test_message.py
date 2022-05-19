from dataclasses import FrozenInstanceError
import pytest

from pydamain.domain.messages.base import (
    Message,
    MessageCatchContext,
    get_issued_messages,
)
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
    with MessageCatchContext():
        issue(m1)
        issue(m2)
        issue(m2)
        messages = get_issued_messages()
    assert {m1, m2} == messages


def test_hook_without_catcher_raise_exception():
    m = ExampleMessage(name="any")
    with pytest.raises(LookupError):
        issue(m)
