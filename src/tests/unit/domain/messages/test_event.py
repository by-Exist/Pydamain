from dataclasses import FrozenInstanceError
from typing import Any, ClassVar
from typing_extensions import Self
import pytest

from pydamain.domain.messages import Event, event, EventHandlers


async def example_event_handler_one(evt: "ExampleEvent", **_: Any):
    return 1


async def example_event_handler_two(evt: "ExampleEvent", **_: Any):
    return 2


@event
class ExampleEvent(Event):

    handlers_: ClassVar[EventHandlers[Self]] = [
        example_event_handler_one,
        example_event_handler_two,
    ]

    name: str


def test_frozen():
    evt = ExampleEvent(name="foo")
    with pytest.raises(FrozenInstanceError):
        evt.name = "bar"


async def test_handle():
    evt = ExampleEvent(name="foo")
    result = await evt.handle_({})
    assert result == [1, 2]
