from typing import TYPE_CHECKING, Protocol, TypeAlias, TypeVar

if TYPE_CHECKING:
    from ...domain.messages import Event


I = TypeVar("I", contravariant=True)
E: TypeAlias = Event


class OutBox(Protocol[I]):
    async def set(self, event: E) -> None:
        ...

    async def del_(self, id: I) -> None:
        ...
