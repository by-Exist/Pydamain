from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing_extensions import dataclass_transform
import orjson

from .event import Event
from ..converter import converter


@dataclass(frozen=True, kw_only=True, slots=True)
class PublicEvent(Event, metaclass=ABCMeta):
    @property
    @abstractmethod
    def from_(self) -> bytes:
        ...

    def dumps_(self) -> bytes:
        return orjson.dumps(converter.unstructure(self))  # type: ignore


@dataclass_transform(
    eq_default=True,
    order_default=False,
    kw_only_default=True,
    field_descriptors=(field,),
)
def public_event(cls: type[PublicEvent]):  # type: ignore
    assert issubclass(cls, PublicEvent)
    return dataclass(cls, frozen=True, kw_only=True, slots=True)  # type: ignore
