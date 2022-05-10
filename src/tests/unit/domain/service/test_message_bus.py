from __future__ import annotations

from dataclasses import dataclass

from typing import Any, ClassVar
from typing_extensions import Self

from pydamain.domain.messages import (
    Command,
    CommandHandler,
    Event,
    EventHandlers,
    issue,
)
from pydamain.domain.service import MessageBus


async def example_command_handler(
    cmd: ExampleCommand, example_command_switch: Switch, **_: Any
):
    example_command_switch.on()
    issue(ExampleEvent())
    return "success"


class ExampleCommand(Command):

    HANDLER: ClassVar[CommandHandler[Self]] = example_command_handler


async def example_event_handler_one(
    evt: ExampleEvent, example_event_switch_one: Switch, **_: Any
):
    example_event_switch_one.on()


async def example_event_handler_two(
    evt: ExampleEvent, example_event_switch_two: Switch, **_: Any
):
    example_event_switch_two.on()


class ExampleEvent(Event):

    HANDLERS: ClassVar[EventHandlers[Self]] = [
        example_event_handler_one,
        example_event_handler_two,
    ]


@dataclass
class Switch:

    is_on: bool = False

    def on(self):
        self.is_on = True


async def test_handle_without_return_hooked_task():
    command_switch = Switch()
    event_switch_one = Switch()
    event_switch_two = Switch()
    bus = MessageBus(
        deps={
            "example_command_switch": command_switch,
            "example_event_switch_one": event_switch_one,
            "example_event_switch_two": event_switch_two,
        }
    )
    result = await bus.handle(ExampleCommand())
    assert result == "success"
    assert command_switch.is_on == True
    assert event_switch_one.is_on == True
    assert event_switch_two.is_on == True


async def test_handle_with_return_hooked_task():
    command_switch = Switch()
    event_switch_one = Switch()
    event_switch_two = Switch()
    bus = MessageBus(
        deps={
            "example_command_switch": command_switch,
            "example_event_switch_one": event_switch_one,
            "example_event_switch_two": event_switch_two,
        }
    )
    result, task = await bus.handle(ExampleCommand(), return_hooked_task=True)
    assert result == "success"
    assert command_switch.is_on == True
    assert event_switch_one.is_on == False
    assert event_switch_two.is_on == False
    await task
    assert event_switch_one.is_on == True
    assert event_switch_two.is_on == True
