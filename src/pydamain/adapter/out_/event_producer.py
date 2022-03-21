from typing import Any, ClassVar
import orjson

from aiokafka import AIOKafkaProducer  # type: ignore

from pydantic import BaseModel

from pydamain.domain.message import Event
from pydamain.port.out_.event_producer import AbstractEventProducer


def orjson_dumps(v: Any, *, default: Any):
    return orjson.dumps(v, default).decode()


class KafkaEvent(BaseModel):
    event_type: str
    event_data: str

    class Config:
        validate_all = True
        allow_mutation = False
        allow_population_by_field_name = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps


def event_to_jsonb(event: Event):
    kafka_event = KafkaEvent(
        event_type=type(event).__name__, event_data=event.json()
    )
    return kafka_event.json().encode("utf-8")


def jsonb_to_event(jsonb: bytes):
    json = jsonb.decode("utf-8")
    kafka_event = KafkaEvent.parse_raw(json)
    event_cls = Event.__event_subclass_registry__[kafka_event.event_type]
    return event_cls.parse_raw(kafka_event.event_data)


class BaseKafkaEventProducer(AbstractEventProducer):

    host: ClassVar[str]
    port: ClassVar[int]
    topic: ClassVar[str]

    def __init__(self) -> None:
        self.aiokafka_producer = AIOKafkaProducer(
            bootstrap_servers=f"{self.host}:{self.port}",
            value_serializer=event_to_jsonb,
            compression_type="lz4",
            enable_idempotence=True,  # 멱등성
        )

    def pre_send(self, event: Event):
        ...

    def post_send(self, event: Event):
        ...

    async def send(self, event: Event, key: int | None = None):
        self.pre_send(event)
        await self.aiokafka_producer.send(  # type: ignore
            topic=self.topic, key=key, value=event
        )
        self.post_send(event)
