from dataclasses import dataclass, field
from typing import Any, ClassVar, Optional, Protocol, TypeVar

from motor.motor_asyncio import (  # type: ignore
    AsyncIOMotorClient,  # type: ignore
    AsyncIOMotorClientSession,  # type: ignore
    AsyncIOMotorCollection,  # type: ignore
    AsyncIOMotorDatabase,  # type: ignore
)
from bson.objectid import ObjectId  # type: ignore

from ....port.out_.repository import Repository, AggregateType


T = TypeVar("T")


class _Converter(Protocol[T]):
    def structure(self, _data: dict[str, Any]) -> T:
        ...

    def unstructure(self, _obj: T) -> dict[str, Any]:
        ...


Converter = _Converter[T]


# https://www.mongodb.com/docs/manual/core/transactions/
@dataclass
class BaseMotorRepository(Repository[AggregateType, ObjectId]):

    AGGREGATE_TYPE: ClassVar[type[AggregateType]]  # type: ignore
    DATABASE_NAME: ClassVar[str] = "default"
    COLLECTION_NAME: ClassVar[str] = None  # type: ignore

    IDENTITY_FACTORY: ClassVar[type[ObjectId]] = ObjectId
    CONVERTER: ClassVar[Converter[AggregateType]]  # type: ignore

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

    async def get(self, id: ObjectId) -> Optional[AggregateType]:
        doc: Optional[dict[str, Any]] = await self.collection.find_one({"_id": id})  # type: ignore
        if not doc:
            return None
        return self.CONVERTER.structure(doc)

    async def set(self, aggregate: AggregateType) -> None:
        doc: dict[str, Any] = self.CONVERTER.unstructure(aggregate)  # type: ignore
        doc["_id"] = aggregate.identity
        await self.collection.insert_one(doc, session=self.session)  # type: ignore

    async def next_identity(self):
        return self.IDENTITY_FACTORY()
