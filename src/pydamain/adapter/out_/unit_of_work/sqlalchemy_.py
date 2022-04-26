from dataclasses import dataclass, field
from typing import Any, Callable, ClassVar

from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore

from ....port.out_.unit_of_work import UnitOfWork, NotInUOWContextError


@dataclass
class BaseSQLAlchemyUnitOfWork(UnitOfWork):

    SESSION_FACTORY: ClassVar[Callable[[], AsyncSession]]

    _in_context: bool = field(default=False, init=False)
    _session: AsyncSession = field(init=False)

    async def __aenter__(self):
        self._in_context = True
        self._session = self.SESSION_FACTORY()
        return await super().__aenter__()

    async def __aexit__(self, *args: Any):
        await super().__aexit__(*args)
        await self._session.close()  # type: ignore
        self._in_context = False

    async def commit(self):
        if not self._in_context:
            raise NotInUOWContextError()
        await self._session.commit()  # type: ignore

    async def rollback(self):
        if not self._in_context:
            raise NotInUOWContextError()
        await self._session.rollback()  # type: ignore
