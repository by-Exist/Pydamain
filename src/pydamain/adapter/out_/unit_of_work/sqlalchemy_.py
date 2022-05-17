from dataclasses import dataclass, field
from types import TracebackType
from typing import Callable, Optional

from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore

from ....port.out_.unit_of_work import UnitOfWorkProtocol


@dataclass
class BaseSQLAlchemyUnitOfWork(UnitOfWorkProtocol):

    SESSION_FACTORY: Callable[[], AsyncSession]

    _session: AsyncSession = field(init=False)

    async def __aenter__(self):
        self._session = self.SESSION_FACTORY()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ):
        await self._session.close()  # type: ignore

    async def commit(self):
        await self._session.commit()  # type: ignore

    async def rollback(self):
        await self._session.rollback()  # type: ignore
