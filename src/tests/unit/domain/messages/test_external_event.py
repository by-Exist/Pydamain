from dataclasses import FrozenInstanceError
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
    name: str

    @property
    def from_(self):
        return bytes()


@command
class ExampleCommand(Command):
    name: str


@external_event
class ExampleExternalEvent(ExternalEvent):
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
    jsonb = ExamplePublicEvent(name="blabla...").dumps_()
    ExampleExternalEvent.loads_(jsonb)


def test_build_commands():
    origin_name = "BlaBla..."
    public_event = ExamplePublicEvent(name=origin_name)
    message_jsonb = public_event.dumps_()
    external_event = ExampleExternalEvent.loads_(message_jsonb)
    cmd = external_event.build_commands_()[0]
    assert cmd.name == origin_name
