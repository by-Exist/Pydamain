from dataclasses import dataclass, field
from typing import Any, Callable, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from ....port.out_.repository import (
    CollectionOrientedRepositoryProtocol,
    AggregateType,
    IdentityType,
)


@dataclass
class BaseSQLAlchemyRepository(
    CollectionOrientedRepositoryProtocol[AggregateType, IdentityType]
):

    AGGREGATE_TYPE: type[AggregateType] = field(init=False)
    IDENTITY_FACTORY: Callable[[], IdentityType] = field(init=False)

    _session: AsyncSession

    async def get(self, id: Any) -> Optional[AggregateType]:
        return await self._session.get(self.AGGREGATE_TYPE, id)  # type: ignore

    async def add(self, aggregate: AggregateType) -> None:
        self._session.add(aggregate)  # type: ignore

    async def delete(self, aggregate: AggregateType) -> None:
        await self._session.delete(aggregate)  # type: ignore

    def next_identity(self) -> IdentityType:
        return self.IDENTITY_FACTORY()
