from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Optional
from sqlalchemy.ext.asyncio import AsyncSession


from ...port.out_.repository import Repository

if TYPE_CHECKING:
    from ...domain.models.main import Aggregate, EntityID


@dataclass
class BaseSQLAlchemyRepository(Repository[EntityID]):

    AGGREGATE_TYPE: ClassVar[type[Aggregate[EntityID]]]  # type: ignore

    session: AsyncSession

    async def get(self, id: EntityID) -> Optional[Aggregate[EntityID]]:
        return await self.session.get(self.AGGREGATE_TYPE, id)  # type: ignore

    async def set(self, aggregate: Aggregate[EntityID]) -> None:
        self.session.add(aggregate)  # type: ignore
