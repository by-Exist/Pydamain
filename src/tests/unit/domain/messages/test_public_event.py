from dataclasses import FrozenInstanceError

import pytest

from pydamain.domain.messages import PublicEvent, public_event


@public_event
class ExamplePublicEvent(PublicEvent):
    name: str

    @property
    def from_(self):
        return None


def test_frozen():
    evt = ExamplePublicEvent(name="foo")
    with pytest.raises(FrozenInstanceError):
        evt.name = "other"
