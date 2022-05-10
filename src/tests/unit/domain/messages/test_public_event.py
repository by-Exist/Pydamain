from dataclasses import FrozenInstanceError
from typing import ClassVar

from cattrs.preconf.orjson import make_converter  # type: ignore
from cattr.preconf.orjson import OrjsonConverter  # type: ignore
import pytest

from pydamain.domain.messages import (
    PublicEvent,
)


class ExamplePublicEvent(PublicEvent):

    name: str

    _converter: ClassVar[OrjsonConverter] = make_converter()

    def dumps_(self) -> bytes:
        return self._converter.dumps(self)  # type: ignore


def test_frozen():
    evt = ExamplePublicEvent(name="foo")
    with pytest.raises(FrozenInstanceError):
        evt.name = "other"


def test_dumps():
    public_event = ExamplePublicEvent(name="foo")
    jsonb = public_event.dumps_()
    assert isinstance(jsonb, bytes)
