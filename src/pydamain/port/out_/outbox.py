from typing import Protocol, TypeVar

from ...domain.messages.event import Event


IdentityType = TypeVar("IdentityType", contravariant=True)


class OutboxProtocol(Protocol):
    async def put(self, _event: Event) -> None:
        ...

    async def delete(self, _event: Event) -> None:
        ...
