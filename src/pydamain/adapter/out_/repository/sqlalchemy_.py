from dataclasses import dataclass
from typing import Any, Callable, Optional
from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore

from ....port.out_.repository import (
    CollectionOrientedRepository,
    AggregateType,
    IdentityType,
)


@dataclass
class BaseSQLAlchemyRepository(
    CollectionOrientedRepository[AggregateType, IdentityType]
):

    AGGREGATE_TYPE: type[AggregateType]
    IDENTITY_FACTORY: Callable[[], IdentityType]

    session: AsyncSession

    async def get(self, id: Any) -> Optional[AggregateType]:
        return await self.session.get(self.AGGREGATE_TYPE, id)  # type: ignore

    async def add(self, aggregate: AggregateType) -> None:
        self.session.add(aggregate)  # type: ignore

    async def delete(self, _aggregate: AggregateType) -> None:
        await self.session.delete(_aggregate)  # type: ignore

    async def next_identity(self) -> IdentityType:
        return self.IDENTITY_FACTORY()
