from abc import abstractmethod
from dataclasses import dataclass, field
from types import TracebackType
from typing import Optional, Protocol
from typing_extensions import Self


class NotInUOWContextError(RuntimeError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args, "can't call without uow context.")


@dataclass
class UnitOfWork(Protocol):

    _in_context: bool = field(default=False, init=False)
    _committed: bool = field(default=False, init=False)

    @abstractmethod
    async def __aenter__(self) -> Self:
        self._in_context = True
        return self

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        if not self._committed:
            await self.rollback()
        self._in_context = False

    @abstractmethod
    async def commit(self) -> None:
        if not self._in_context:
            raise NotInUOWContextError()
        self._committed = True

    @abstractmethod
    async def rollback(self) -> None:
        if not self._in_context:
            raise NotInUOWContextError()
