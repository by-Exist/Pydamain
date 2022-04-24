from abc import ABCMeta, abstractmethod
from contextvars import ContextVar
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, ClassVar, Optional, TypeVar
from uuid import UUID, uuid4
import orjson

from typing_extensions import Self, dataclass_transform

from ..handler import Handler, Handlers

from ..converter import converter


# ============================================================================
# Message
# ============================================================================
@dataclass(frozen=True, kw_only=True, slots=True)
class Message:
    id: UUID = field(default_factory=uuid4)
    create_time: datetime = field(default_factory=datetime.now)


# ============================================================================
# Command
# ============================================================================
C = TypeVar("C", bound="Command")
CommandHandler = Handler[C, Any]


@dataclass(frozen=True, kw_only=True, slots=True)
class Command(Message):

    handler: ClassVar[CommandHandler[Self] | None] = None


@dataclass_transform(
    eq_default=True,
    order_default=False,
    kw_only_default=True,
    field_descriptors=(field,),
)
def command(cls: type[Command]):  # type: ignore
    assert issubclass(cls, Command)
    return dataclass(cls, frozen=True, kw_only=True, slots=True)  # type: ignore


# ============================================================================
# Event
# ============================================================================
E = TypeVar("E", bound="Event")
EventHandler = Handler[E, None]
EventHandlers = Handlers[E, None]


@dataclass(frozen=True, kw_only=True, slots=True)
class Event(Message):

    handlers: ClassVar[EventHandlers[Self]] = []

    def issue(self):
        events = events_context_var.get()
        events.append(self)


@dataclass_transform(
    eq_default=True,
    order_default=False,
    kw_only_default=True,
    field_descriptors=(field,),
)
def event(cls: type[Event]):  # type: ignore
    assert issubclass(cls, Event)
    return dataclass(cls, frozen=True, kw_only=True, slots=True)  # type: ignore


events_context_var: ContextVar[list[Event]] = ContextVar("events")


# ============================================================================
# Public Event
# ============================================================================
@dataclass(frozen=True, kw_only=True, slots=True)
class PublicEvent(Event):
    from_: Optional[UUID] = None

    def dumps(self):
        return orjson.dumps(converter.unstructure(self))  # type: ignore

    @classmethod
    def loads(cls, jsonb: bytes):
        return converter.structure(orjson.loads(jsonb), cls)


@dataclass_transform(
    eq_default=True,
    order_default=False,
    kw_only_default=True,
    field_descriptors=(field,),
)
def public_event(cls: type[PublicEvent]):  # type: ignore
    assert issubclass(cls, PublicEvent)
    return dataclass(cls, frozen=True, kw_only=True, slots=True)  # type: ignore


# ============================================================================
# External Event
# ============================================================================
@dataclass(frozen=True, kw_only=True, slots=True)
class ExternalEvent(Event, metaclass=ABCMeta):
    @classmethod
    def loads(cls, jsonb: bytes):
        return converter.structure(orjson.loads(jsonb), cls)

    @abstractmethod
    def build_commands(self) -> list[Command]:
        ...


@dataclass_transform(
    eq_default=True,
    order_default=False,
    kw_only_default=True,
    field_descriptors=(field,),
)
def external_event(cls: type[ExternalEvent]):  # type: ignore
    assert issubclass(cls, ExternalEvent)
    return dataclass(cls, frozen=True, kw_only=True, slots=True)  # type: ignore
