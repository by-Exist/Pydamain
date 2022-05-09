from typing import Any, Protocol


from ...domain.messages import Event


class OutBox(Protocol):
    async def set(self, _event: Event) -> None:
        ...

    async def del_(self, _id: Any) -> None:
        ...
