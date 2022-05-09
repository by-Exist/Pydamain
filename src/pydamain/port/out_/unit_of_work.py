from abc import abstractmethod
from dataclasses import dataclass
from types import TracebackType
from typing import Optional, Protocol
from typing_extensions import Self


@dataclass
class UnitOfWork(Protocol):
    @abstractmethod
    async def __aenter__(self) -> Self:
        ...

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        ...

    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def rollback(self) -> None:
        ...
