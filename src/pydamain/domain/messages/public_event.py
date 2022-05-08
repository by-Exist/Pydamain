from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from typing_extensions import dataclass_transform

from .event import Event


@dataclass(frozen=True, kw_only=True, slots=True)
class PublicEvent(Event):
    @property
    def from_(self) -> Optional[bytes]:
        return None

    @abstractmethod
    def dumps_(self) -> bytes:
        ...


@dataclass_transform(
    eq_default=True,
    order_default=False,
    kw_only_default=True,
    field_descriptors=(field,),
)
def public_event(cls: type[PublicEvent]):  # type: ignore
    assert issubclass(cls, PublicEvent)
    return dataclass(cls, frozen=True, kw_only=True, slots=True)  # type: ignore
