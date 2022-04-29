from abc import ABCMeta, abstractmethod
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, ClassVar, Optional, TypeVar

from typing_extensions import Self, dataclass_transform

import orjson

from ..converter import converter
from ..handler import Handler, Handlers

if TYPE_CHECKING:
    from .command import Command


# ============================================================================
# Event
# ============================================================================
E = TypeVar("E", bound="Event")
EventHandler = Handler[E, None]
EventHandlers = Handlers[E, None]


@dataclass(frozen=True, kw_only=True, slots=True)
class Event(metaclass=ABCMeta):

    handlers: ClassVar[EventHandlers[Self]] = []

    @property
    @abstractmethod
    def identity(self) -> Any:
        ...

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
class PublicEvent(Event, metaclass=ABCMeta):
    @property
    @abstractmethod
    def from_(self) -> Optional[Any]:
        ...

    def dumps(self) -> bytes:
        return orjson.dumps(converter.unstructure(self))  # type: ignore

    @classmethod
    def loads(cls, jsonb: bytes) -> Self:
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
    def build_commands(self) -> list["Command"]:
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
