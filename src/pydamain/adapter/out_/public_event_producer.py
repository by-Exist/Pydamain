from dataclasses import dataclass, field
from typing import TYPE_CHECKING, ClassVar, Optional, cast

from aiokafka import AIOKafkaProducer  # type: ignore
from aiokafka.structs import RecordMetadata  # type: ignore

from ...port.out_.public_event_producer import PublicEventProducer


if TYPE_CHECKING:
    from ...domain.messages import PublicEvent


@dataclass
class BaseKafkaPublicEventProducer(PublicEventProducer):

    BOOTSTRAP_SERVERS: ClassVar[list[str]]
    TOPIC_PREFIX: ClassVar[list[str]]

    _aiokafka_producer: AIOKafkaProducer = field(init=False)

    def __post_init__(self):
        self._aiokafka_producer = AIOKafkaProducer(
            bootstrap_servers=self.BOOTSTRAP_SERVERS,
            enable_idempotence=True,
        )

    async def pre_produce(self, msg: PublicEvent):
        ...

    async def post_produce(self, msg: PublicEvent):
        ...

    async def produce(self, public_event: PublicEvent):
        await self._aiokafka_producer.start()
        await self.pre_produce(public_event)
        record_metadata = await self._aiokafka_producer.send_and_wait(  # type: ignore
            topic=self.generate_topic_name(public_event),
            key=self.generate_key(public_event),
            value=self.generate_value(public_event),
        )
        record_metadata = cast(RecordMetadata, record_metadata)
        await self.post_produce(public_event)
        await self._aiokafka_producer.stop()

    @classmethod
    def generate_topic_name(cls, public_event: PublicEvent) -> str:
        return f"{cls.TOPIC_PREFIX}/{type(public_event).__name__}"

    @classmethod
    def generate_key(cls, public_event: PublicEvent) -> Optional[bytes]:
        return public_event.from_ if public_event.from_ else None

    @classmethod
    def generate_value(cls, public_event: PublicEvent) -> bytes:
        return public_event.dump_()
