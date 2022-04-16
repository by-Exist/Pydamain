from typing import TYPE_CHECKING, Any, Optional, Protocol, TypeVar


if TYPE_CHECKING:
    from ...domain.models.main import Aggregate


A = TypeVar("A", bound=Aggregate)


class Repository(Protocol[A]):
    async def get(self, id: Any) -> Optional[A]:
        ...

    async def set(self, aggregate: A) -> None:
        ...
