from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing_extensions import dataclass_transform
import orjson

from .command import Command
from .event import Event
from ..converter import converter


@dataclass(frozen=True, kw_only=True, slots=True)
class ExternalEvent(Event, metaclass=ABCMeta):
    @classmethod
    def loads_(cls, jsonb: bytes):
        return converter.structure(orjson.loads(jsonb), cls)

    @abstractmethod
    def build_commands_(self) -> tuple[Command, ...]:
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
