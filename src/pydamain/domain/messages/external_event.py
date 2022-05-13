from abc import abstractmethod
from typing_extensions import Self

from .command import Command
from .event import Event


class ExternalEvent(Event):
    @classmethod
    @abstractmethod
    def load_(cls, jsonb: bytes) -> Self:
        ...

    @abstractmethod
    def build_commands_(self) -> tuple[Command, ...]:
        ...
