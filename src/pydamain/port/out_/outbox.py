from typing import Protocol, TypeVar


EventType = TypeVar("EventType", contravariant=True)
AggregateType = TypeVar("AggregateType", contravariant=True)


class OutboxProtocol(Protocol[EventType, AggregateType]):
    async def put(self, _event: EventType, _aggregate: AggregateType) -> None:
        ...

    async def delete(self, _event: EventType) -> None:
        ...
