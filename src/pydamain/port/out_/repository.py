from typing import TYPE_CHECKING, Any, Optional, Protocol, TypeVar


if TYPE_CHECKING:
    from ...domain.models import Aggregate


A = TypeVar("A", bound=Aggregate)


class Repository(Protocol[A]):
    async def get(self, _id: Any) -> Optional[A]:
        ...

    async def set(self, _aggregate: A) -> None:
        ...
