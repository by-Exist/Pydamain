from typing import TYPE_CHECKING, Any, Protocol


if TYPE_CHECKING:
    from ...domain.messages import Event


class OutBox(Protocol):
    async def set(self, event: Event) -> None:
        ...

    async def del_(self, id: Any) -> None:
        ...
