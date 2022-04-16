from typing import TYPE_CHECKING, Optional, Protocol


if TYPE_CHECKING:
    from ...domain.models.main import EntityID, Aggregate


class Repository(Protocol[EntityID]):
    async def get(self, id: EntityID) -> Optional[Aggregate[EntityID]]:
        ...

    async def set(self, aggregate: Aggregate[EntityID]) -> None:
        ...
