from typing import TYPE_CHECKING, Optional, Protocol, TypeVar


if TYPE_CHECKING:
    from ...domain.models import Aggregate


AggregateType = TypeVar("AggregateType", bound=Aggregate)
IdentityType = TypeVar("IdentityType")


class CollectionOrientedRepository(Protocol[AggregateType, IdentityType]):
    async def add(self, _aggregate: AggregateType) -> None:
        ...

    async def get(self, _id: IdentityType) -> Optional[AggregateType]:
        ...

    async def delete(self, _aggregate: AggregateType) -> None:
        ...

    async def next_identity(self) -> IdentityType:
        ...


class PersistenceOrientedRepository(Protocol[AggregateType, IdentityType]):
    async def save(self, _aggregate: AggregateType) -> None:
        ...

    async def get(self, _id: IdentityType) -> Optional[AggregateType]:
        ...

    async def delete(self, _aggregate: AggregateType) -> None:
        ...

    async def next_identity(self) -> IdentityType:
        ...
