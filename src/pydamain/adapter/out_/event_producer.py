from typing import ClassVar

from aiokafka import AIOKafkaProducer  # type: ignore

from pydantic import BaseModel

from pydamain.domain.model import Aggregate
from pydamain.domain.message import Event
from pydamain.port.out_.event_producer import AbstractEventProducer


def serialize_key_from_aggregate(aggregate: Aggregate | None):
    if aggregate:
        return "{}: {}".format(
            type(aggregate).__name__, aggregate.id.hex.encode("utf-8")
        )


def serialize_value_from_event(event: Event):
    return event.json(by_alias=True).encode("utf-8")


class KafkaEvent(BaseModel):
    event_type: str
    event: Event


class BaseKafkaEventProducer(AbstractEventProducer):

    host: ClassVar[str]
    port: ClassVar[int]
    topic: ClassVar[str]

    def __init__(self) -> None:
        self.aiokafka_producer = AIOKafkaProducer(
            bootstrap_servers=f"{self.host}:{self.port}",
            key_serializer=serialize_key_from_aggregate,
            value_serializer=serialize_value_from_event,
            compression_type="lz4",
            enable_idempotence=True,  # 멱등성
        )

    def pre_send(self, event: Event):
        ...

    def post_send(self, event: Event):
        ...

    async def send(self, event: Event):
        self.pre_send(event)
        await self.aiokafka_producer.send(  # type: ignore
            topic=self.topic,
            key=event.from_,
            value=KafkaEvent(
                event_type=type(event).__name__,
                event=event,
            ),
        )
        self.post_send(event)
