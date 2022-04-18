from dataclasses import dataclass, field
from typing import Any, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from ...port.out_.unit_of_work import UnitOfWork


@dataclass
class BaseSQLAlchemyUnitOfWork(UnitOfWork):

    SESSION_FACTORY: Callable[[], AsyncSession]

    _session: AsyncSession = field(init=False)

    def __post_init__(self):
        self._session = self.SESSION_FACTORY()

    async def __aexit__(self, *args: Any):
        await super().__aexit__(*args)
        await self._session.close()  # type: ignore

    async def commit(self):
        await self._session.commit()  # type: ignore

    async def rollback(self):
        await self._session.rollback()  # type: ignore
