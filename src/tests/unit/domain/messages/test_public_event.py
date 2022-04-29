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


@public_event
class ConvertExample(PublicEvent):
    a: typing.Any = 1
    b: int = 1
    c: float = 1.0
    d: str = "string"
    e: bytes = b"bytes"
    f: CardSuit = CardSuit.DIAMOND
    g: typing.Any | None = 1

    h: typing.Optional[int] = 1
    i: typing.Optional[float] = 1.0
    j: typing.Optional[str] = "string"
    k: typing.Optional[bytes] = b"bytes"
    l: typing.Optional[CardSuit] = CardSuit.DIAMOND

    m: list[int] = field(default_factory=lambda: [1, 2, 3])
    n: tuple[int, ...] = (1, 2, 3)
    o: tuple[int, float] = (1, 2.0)
    p: set[int] = field(default_factory=lambda: {1, 2, 3})
    q: frozenset[int] = frozenset([1, 2, 3])
    r: dict[str, int] = field(default_factory=lambda: {"key": 1})

    s: Inner = Inner()

    t: UUID = field(default_factory=uuid4)
    u: datetime = field(default_factory=datetime.now)
    v: date = field(default_factory=datetime.now().date)
    w: time = field(default_factory=datetime.now().time)

    id: UUID = field(default_factory=uuid4)

    @property
    def identity(self):
        return self.id


i = uuid4()
t = datetime.now()


class TestPublicEvent:

    foo_1 = Example(id=i, name="foo")
    foo_2 = Example(id=i, name="foo")
    foo_3 = Example(id=i, name="bar")
    bar = Example(name="bar")
    c = ConvertExample()

    def test_event_eq(self):
        assert self.foo_1 == self.foo_2
        assert self.foo_1 != self.foo_3

    def test_event_frozen(self):
        with pytest.raises(FrozenInstanceError):
            self.bar.name = "other"

    def test_convert(self):
        raw = self.c.dumps()
        c = ConvertExample.loads(raw)
        assert isinstance(raw, bytes)
        assert self.c == c
