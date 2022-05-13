from abc import abstractmethod
from typing import Optional

from .event import Event


class PublicEvent(Event):
    @property
    def from_(self) -> Optional[bytes]:
        return None

    @abstractmethod
    def dump_(self) -> bytes:
        ...
