from typing import Optional, TypeVar
import asyncio

from beanie import PydanticObjectId, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore

from pydamain.domain.model.beanie_ import Aggregate
from pydamain.port.out_.repository import AbstractPersistenceRepository


A = TypeVar("A", bound=Aggregate)


class BaseBeanieRepository(AbstractPersistenceRepository[A, PydanticObjectId]):

    database_uri: str

    aggregate_class: type[A]

    def __init__(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            init_beanie(
                database=AsyncIOMotorClient(self.database_uri),
                document_models=[self.aggregate_class],
            )
        )

    async def save(
        self,
        _aggregate: A,
    ):
        await self.aggregate_class.insert_one(_aggregate)

    async def get(
        self,
        _identity: PydanticObjectId,
    ) -> Optional[A]:
        return await self.aggregate_class.get(_identity)  # type: ignore
