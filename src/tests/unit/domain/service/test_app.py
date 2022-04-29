from __future__ import annotations

from dataclasses import dataclass

from typing import Any, ClassVar
from typing_extensions import Self
from uuid import UUID, uuid4

from pydamain.domain.messages import (
    Command,
    CommandHandler,
    Event,
    EventHandlers,
    command,
    event,
    field,
)
from pydamain.domain.service import DomainApplication


# handlers
async def example_cmd_handler(cmd: ExampleCommand, switch: Switch, **_: Any):
    switch.on()
    ExampleEvent().issue()
    return "success"


async def example_evt_handler_one(evt: ExampleEvent, one: Switch, **_: Any):
    one.on()


async def example_evt_handler_two(evt: ExampleEvent, two: Switch, **_: Any):
    two.on()


# commands
@command
class ExampleCommand(Command):

    id: UUID = field(default_factory=uuid4)

    handler: ClassVar[CommandHandler[Self]] = example_cmd_handler

    @property
    def identity(self) -> Any:
        return self.id


# events
@event
class ExampleEvent(Event):

    id: UUID = field(default_factory=uuid4)

    handlers: ClassVar[EventHandlers[Self]] = [
        example_evt_handler_one,
        example_evt_handler_two,
    ]

    @property
    def identity(self) -> Any:
        return self.id


# switch (run check)
@dataclass
class Switch:

    state: bool = False

    def on(self):
        self.state = True


switch_1 = Switch()
switch_2 = Switch()
switch_3 = Switch()


app = DomainApplication(
    cmd_deps={"switch": switch_1},
    evt_deps={
        "one": switch_2,
        "two": switch_3,
    },
)


class TestDomainApplication:
    async def test_app(self):
        cmd = ExampleCommand()
        result = await app.handle(cmd)
        assert result == "success"
        assert switch_1.state == True
        assert switch_2.state == True
        assert switch_3.state == True
