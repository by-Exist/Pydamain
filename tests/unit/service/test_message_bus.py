from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pydamain.domain.messages import Message
from pydamain.service import MessageBus, issue


class Command(Message):
    ...


class Event(Message):
    ...


async def example_command_handler(
    cmd: ExampleCommand, example_command_switch: Switch, **_: Any
):
    example_command_switch.on()
    issue(ExampleEvent())
    return "success"


class ExampleCommand(Command):
    ...


async def example_event_handler_one(
    evt: ExampleEvent, example_event_switch_one: Switch, **_: Any
):
    example_event_switch_one.on()


async def example_event_handler_two(
    evt: ExampleEvent, example_event_switch_two: Switch, **_: Any
):
    example_event_switch_two.on()


class ExampleEvent(Event):
    ...


@dataclass
class Switch:

    is_on: bool = False

    def on(self):
        self.is_on = True


async def test_handle():
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
    bus.register(ExampleCommand, example_command_handler)
    bus.register(ExampleEvent, (example_event_handler_one, example_event_handler_two))
    result = await bus.dispatch(ExampleCommand())
    assert result == "success"
    assert command_switch.is_on == True
    assert event_switch_one.is_on == True
    assert event_switch_two.is_on == True


async def test_hook():
    command_switch = Switch()
    pre_hook_switch = Switch()
    post_hook_switch = Switch()

    async def pre_hook(msg: Any, handler: Any):
        pre_hook_switch.on()

    async def post_hook(msg: Any, handler: Any):
        post_hook_switch.on()

    bus = MessageBus(
        deps={
            "example_command_switch": command_switch,
        },
        pre_hook=pre_hook,
        post_hook=post_hook,
    )
    bus.register(ExampleCommand, example_command_handler)
    await bus.dispatch(ExampleCommand())
    assert pre_hook_switch.is_on
    assert post_hook_switch.is_on


async def test_handle_with_return_hooked_task():
    command_switch = Switch()
    event_switch_one = Switch()
    event_switch_two = Switch()
    bus = MessageBus(
        deps={
            "example_command_switch": command_switch,
            "example_event_switch_one": event_switch_one,
            "example_event_switch_two": event_switch_two,
        },
    )
    bus.register(ExampleCommand, example_command_handler)
    bus.register(ExampleEvent, (example_event_handler_one, example_event_handler_two))
    result, task = await bus.dispatch(ExampleCommand(), return_hooked_task=True)
    assert result == "success"
    assert command_switch.is_on == True
    assert event_switch_one.is_on == False
    assert event_switch_two.is_on == False
    await task
    assert event_switch_one.is_on == True
    assert event_switch_two.is_on == True
