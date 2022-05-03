from dataclasses import FrozenInstanceError
from typing import Any, ClassVar
from typing_extensions import Self
import pytest

from pydamain.domain.messages import Command, command, CommandHandler


check_handled = False


async def example_command_handler(ex_cmd: "ExampleCommand", some: str, **_: Any):
    global check_handled
    check_handled = True
    return some


@command
class ExampleCommand(Command):

    handler_: ClassVar[CommandHandler[Self]] = example_command_handler

    name: str


def test_frozen():
    foo = ExampleCommand(name="foo")
    with pytest.raises(FrozenInstanceError):
        foo.name = "other"


async def test_handle():
    cmd = ExampleCommand(name="foo")
    result = await cmd.handle_({"some": "value"})
    assert result == "value"
