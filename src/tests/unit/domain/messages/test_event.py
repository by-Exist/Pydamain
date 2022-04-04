from dataclasses import FrozenInstanceError
import pytest
from pydamain.domain.messages.main import Event, event


@event
class Example(Event):
    name: str


class TestEvent:

    foo_1 = Example(name="foo")
    foo_2 = Example(name="foo")
    bar = Example(name="bar")

    def test_event_has_unique_id(self):
        assert self.foo_1 != self.foo_2

    def test_event_frozen(self):
        with pytest.raises(FrozenInstanceError):
            self.bar.name = "other"
