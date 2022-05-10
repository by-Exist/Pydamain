from dataclasses import FrozenInstanceError
from typing import ClassVar
from typing_extensions import Self

from cattrs.preconf.orjson import make_converter  # type: ignore
from cattr.preconf.orjson import OrjsonConverter  # type: ignore
import pytest

from pydamain.domain.messages import (
    Command,
    ExternalEvent,
    PublicEvent,
)


class ExamplePublicEvent(PublicEvent):

    name: str

    _converter: ClassVar[OrjsonConverter] = make_converter()

    @property
    def from_(self):
        return bytes()

    def dumps_(self) -> bytes:
        return self._converter.dumps(self)  # type: ignore


class ExampleCommand(Command):

    name: str


class ExampleExternalEvent(ExternalEvent):

    name: str

    _converter: ClassVar[OrjsonConverter] = make_converter()

    @classmethod
    def loads_(cls, jsonb: bytes) -> Self:
        return cls._converter.loads(jsonb, cls)

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
