from dataclasses import dataclass, field
from typing import Any, ClassVar, Optional

from motor.motor_asyncio import (  # type: ignore
    AsyncIOMotorClient,  # type: ignore
    AsyncIOMotorClientSession,  # type: ignore
    AsyncIOMotorCollection,  # type: ignore
    AsyncIOMotorDatabase,  # type: ignore
)

from ....domain.converter import converter
from ....port.out_.repository import Repository, A


# https://www.mongodb.com/docs/manual/core/transactions/
@dataclass
class BaseMotorRepository(Repository[A]):

    AGGREGATE_TYPE: ClassVar[type[A]]  # type: ignore
    DATABASE_NAME: ClassVar[str] = "default"
    COLLECTION_NAME: ClassVar[str] = None  # type: ignore

    session: AsyncIOMotorClientSession
    collection: AsyncIOMotorCollection = field(init=False)  # type: ignore

    def __init_subclass__(cls) -> None:
        if not cls.AGGREGATE_TYPE:
            raise AttributeError(f"required {cls.__name__}.AGGREGATE_TYPE")
        if not cls.COLLECTION_NAME:
            cls.COLLECTION_NAME = cls.AGGREGATE_TYPE.__name__

    def __post_init__(self):
        client: AsyncIOMotorClient = self.session.client  # type: ignore
        database: AsyncIOMotorDatabase = getattr(client, self.DATABASE_NAME)  # type: ignore
        self.collection: AsyncIOMotorCollection = getattr(
            database, self.COLLECTION_NAME  # type: ignore
        )

    async def get(self, id: Any) -> Optional[A]:
        doc: Optional[dict[str, Any]] = await self.collection.find_one({"_id": id})  # type: ignore
        if not doc:
            return None
        return converter.structure(doc, self.AGGREGATE_TYPE)

    async def set(self, aggregate: A) -> None:
        doc: dict[str, Any] = converter.unstructure(aggregate)  # type: ignore
        doc["_id"] = aggregate.identity
        await self.collection.insert_one(doc, session=self.session)  # type: ignore
