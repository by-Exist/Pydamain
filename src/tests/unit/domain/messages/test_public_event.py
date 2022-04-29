from datetime import date, datetime, time
import typing
from dataclasses import FrozenInstanceError, dataclass, field
from enum import Enum, unique
from uuid import UUID, uuid4

import pytest

from pydamain.domain.messages import PublicEvent, public_event, field


@public_event
class Example(PublicEvent):
    id: UUID = field(default_factory=uuid4)
    name: str

    @property
    def identity(self):
        return self.id


@unique
class CardSuit(Enum):
    CLUB = "club"
    DIAMOND = "diamond"
    HEART = "heart"
    SPADE = "spade"


@dataclass
class Inner:
    foo: str = "foo"


i = uuid4()
t = datetime.now()


class TestPublicEvent:

    foo_1 = Example(id=i, name="foo")
    foo_2 = Example(id=i, name="foo")
    foo_3 = Example(id=i, name="bar")
    bar = Example(name="bar")

    def test_event_eq(self):
        assert self.foo_1 == self.foo_2
        assert self.foo_1 != self.foo_3

    def test_event_frozen(self):
        with pytest.raises(FrozenInstanceError):
            self.bar.name = "other"
