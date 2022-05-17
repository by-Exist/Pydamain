from typing import Protocol, TypeVar
from uuid import UUID

from ...domain.messages.event import Event


IdentityType = TypeVar("IdentityType", contravariant=True)


class Outbox(Protocol):
    async def put(self, _id: UUID, _event: Event) -> None:
        ...

    async def delete(self, _id: UUID) -> None:
        ...
