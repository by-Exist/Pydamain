from dataclasses import FrozenInstanceError
import pytest

from pydamain.domain.messages import Message


class ExampleMessage(Message):
    name: str


def test_frozen():
    evt = ExampleMessage(name="foo")
    with pytest.raises(FrozenInstanceError):
        evt.name = "bar"