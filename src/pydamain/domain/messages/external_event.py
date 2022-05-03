from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar, Protocol, TypeVar
from typing_extensions import dataclass_transform

from .command import Command
from .event import Event


T = TypeVar("T")


class _Loader(Protocol):
    def loads(self, data: bytes, cl: type[T]) -> T:
        ...


Loader = _Loader


@dataclass(frozen=True, kw_only=True, slots=True)
class ExternalEvent(Event, metaclass=ABCMeta):

    LOADER: ClassVar[Loader]

    @classmethod
    def loads_(cls, jsonb: bytes):
        return cls.LOADER.loads(jsonb, cls)

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
