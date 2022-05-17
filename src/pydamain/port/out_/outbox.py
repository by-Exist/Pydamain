from typing import Protocol, TypeVar


EventType = TypeVar("EventType", contravariant=True)


class OutboxProtocol(Protocol[EventType]):
    async def put(self, _event: EventType) -> None:
        ...

    async def delete(self, _event: EventType) -> None:
        ...
