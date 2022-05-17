from typing import Optional, Protocol, TypeVar


AggregateType = TypeVar("AggregateType")
IdentityType = TypeVar("IdentityType")


class CollectionOrientedRepositoryProtocol(Protocol[AggregateType, IdentityType]):
    async def add(self, _aggregate: AggregateType) -> None:
        ...

    async def get(self, _id: IdentityType) -> Optional[AggregateType]:
        ...

    async def delete(self, _aggregate: AggregateType) -> None:
        ...

    def next_identity(self) -> IdentityType:
        ...


class PersistenceOrientedRepositoryProtocol(Protocol[AggregateType, IdentityType]):
    async def save(self, _aggregate: AggregateType) -> None:
        ...

    async def get(self, _id: IdentityType) -> Optional[AggregateType]:
        ...

    async def delete(self, _aggregate: AggregateType) -> None:
        ...

    def next_identity(self) -> IdentityType:
        ...
