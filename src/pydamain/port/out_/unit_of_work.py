from abc import abstractmethod
from types import TracebackType
from typing import Optional, Protocol
from typing_extensions import Self


class NotInUOWContextError(RuntimeError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args, "can't call without uow context.")


class UnitOfWork(Protocol):
    @abstractmethod
    async def __aenter__(self) -> Self:
        return self

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        await self.rollback()

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError()
