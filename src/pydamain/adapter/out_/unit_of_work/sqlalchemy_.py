from dataclasses import dataclass, field
from types import TracebackType
from typing import Callable, ClassVar, Optional

from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore

from ....port.out_.unit_of_work import UnitOfWork


@dataclass
class BaseSQLAlchemyUnitOfWork(UnitOfWork):

    SESSION_FACTORY: ClassVar[Callable[[], AsyncSession]]

    _session: AsyncSession = field(init=False)

    async def __aenter__(self):
        self._session = self.SESSION_FACTORY()
        return await super().__aenter__()

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ):
        await super().__aexit__(exc_type, exc_value, traceback)
        await self._session.close()  # type: ignore

    async def commit(self):
        await super().commit()
        await self._session.commit()  # type: ignore

    async def rollback(self):
        await super().rollback()
        await self._session.rollback()  # type: ignore
