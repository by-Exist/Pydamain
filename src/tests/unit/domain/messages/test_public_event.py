from dataclasses import FrozenInstanceError
from typing import ClassVar

from cattrs.preconf.orjson import make_converter  # type: ignore
from cattr.preconf.orjson import OrjsonConverter  # type: ignore
import pytest

from pydamain.domain.messages import (
    ExternalEvent,
    PublicEvent,
    external_event,
    public_event,
)


@public_event
class ExamplePublicEvent(PublicEvent):

    DUMPER: ClassVar[OrjsonConverter] = make_converter()

    name: str


@external_event
class ExampleExternalEvent(ExternalEvent):

    LOADER: ClassVar[OrjsonConverter] = make_converter()

    name: str


def test_frozen():
    evt = ExamplePublicEvent(name="foo")
    with pytest.raises(FrozenInstanceError):
        evt.name = "other"


def test_dumps():
    public_event = ExamplePublicEvent(name="foo")
    jsonb = public_event.dumps_()
    assert isinstance(jsonb, bytes)
