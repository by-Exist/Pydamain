from dataclasses import FrozenInstanceError
from typing import ClassVar

from cattrs.preconf.orjson import make_converter  # type: ignore
from cattr.preconf.orjson import OrjsonConverter  # type: ignore
import pytest

from pydamain.domain.messages import (
    Command,
    ExternalEvent,
    PublicEvent,
    command,
    external_event,
    public_event,
)


@public_event
class ExamplePublicEvent(PublicEvent):

    DUMPER: ClassVar[OrjsonConverter] = make_converter()

    name: str

    @property
    def from_(self):
        return bytes()


@command
class ExampleCommand(Command):

    name: str


@external_event
class ExampleExternalEvent(ExternalEvent):

    LOADER: ClassVar[OrjsonConverter] = make_converter()

    name: str

    def build_commands_(self):
        return (
            ExampleCommand(name=self.name),
            Command(),
        )


def test_frozen():
    evt = ExampleExternalEvent(name="foo")
    with pytest.raises(FrozenInstanceError):
        evt.name = "bar"


def test_loads():
    public_event = ExamplePublicEvent(name="blabla...")
    jsonb = public_event.dumps_()
    external_event = ExampleExternalEvent.loads_(jsonb)
    assert external_event.name == public_event.name


def test_build_commands():
    origin_name = "BlaBla..."
    public_event = ExamplePublicEvent(name=origin_name)
    message_jsonb = public_event.dumps_()
    external_event = ExampleExternalEvent.loads_(message_jsonb)
    cmd = external_event.build_commands_()[0]
    assert cmd.name == origin_name
