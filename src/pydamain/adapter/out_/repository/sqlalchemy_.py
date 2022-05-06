from dataclasses import dataclass
from typing import Any, Callable, ClassVar, Optional
from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore

from ....port.out_.repository import Repository, AggregateType, IdentityType


@dataclass
class BaseSQLAlchemyRepository(Repository[AggregateType, IdentityType]):

    AGGREGATE_TYPE: ClassVar[type[AggregateType]]  # type: ignore
    IDENTITY_FACTORY: ClassVar[Callable[[], IdentityType]]  # type: ignore

    session: AsyncSession

    async def get(self, id: Any) -> Optional[AggregateType]:
        return await self.session.get(self.AGGREGATE_TYPE, id)  # type: ignore

    async def set(self, aggregate: AggregateType) -> None:
        self.session.add(aggregate)  # type: ignore

    async def next_identity(self) -> IdentityType:
        return self.IDENTITY_FACTORY()
