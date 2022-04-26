from dataclasses import dataclass
from typing import Any, ClassVar, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from ....port.out_.repository import Repository, A


@dataclass
class BaseSQLAlchemyRepository(Repository[A]):

    AGGREGATE_TYPE: ClassVar[type[A]]  # type: ignore

    session: AsyncSession

    async def get(self, id: Any) -> Optional[A]:
        return await self.session.get(self.AGGREGATE_TYPE, id)  # type: ignore

    async def set(self, aggregate: A) -> None:
        self.session.add(aggregate)  # type: ignore
