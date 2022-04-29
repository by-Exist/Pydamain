from typing import Any, Protocol


from ...domain.messages import PublicEvent


class OutBox(Protocol):
    async def set(self, event: PublicEvent) -> None:
        ...

    async def del_(self, id: Any) -> None:
        ...
