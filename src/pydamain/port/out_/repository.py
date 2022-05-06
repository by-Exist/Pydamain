from typing import TYPE_CHECKING, Any, Optional, Protocol, TypeVar


if TYPE_CHECKING:
    from ...domain.models import Aggregate


AggregateType = TypeVar("AggregateType", bound=Aggregate)
IdentityType = TypeVar("IdentityType", covariant=True)


class Repository(Protocol[AggregateType, IdentityType]):
    async def get(self, _id: Any) -> Optional[AggregateType]:
        ...

    async def set(self, _aggregate: AggregateType) -> None:
        ...

    async def next_identity(self) -> IdentityType:
        ...
