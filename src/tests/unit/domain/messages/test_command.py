from dataclasses import FrozenInstanceError
from typing import Any, ClassVar
from typing_extensions import Self
import pytest

from pydamain.domain.messages import Command, CommandHandler


check_handled = False


async def example_command_handler(cmd: "ExampleCommand", some: str, **_: Any):
    global check_handled
    check_handled = True
    return some


class ExampleCommand(Command):

    HANDLER: ClassVar[CommandHandler[Self]] = example_command_handler

    name: str


def test_frozen():
    foo = ExampleCommand(name="foo")
    with pytest.raises(FrozenInstanceError):
        foo.name = "other"


async def test_handle():
    cmd = ExampleCommand(name="foo")
    result = await cmd.handle_({"some": "value"})  # type: ignore
    assert result == "value"
