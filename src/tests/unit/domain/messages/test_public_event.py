from dataclasses import FrozenInstanceError

import pytest

from pydamain.domain.messages import PublicEvent, public_event


@public_event
class ExamplePublicEvent(PublicEvent):
    name: str


def test_frozen():
    evt = ExamplePublicEvent(name="foo")
    with pytest.raises(FrozenInstanceError):
        evt.name = "other"
