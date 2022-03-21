from typing import Any
from uuid import uuid4
import orjson

from pydantic import UUID4, BaseModel, Field


def orjson_dumps(v: Any, *, default: Any):
    return orjson.dumps(v, default).decode()


class BaseDomainModel(BaseModel):
    class Config(BaseModel.Config):
        validate_all = True
        allow_population_by_field_name = True
        validate_assignment = True
        orm_mode = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class ValueObject(BaseDomainModel):
    class Config(BaseDomainModel.Config):
        allow_mutation = False

    def __eq__(self, other: Any):
        if isinstance(other, type(self)):
            return self.__dict__ == other.__dict__
        return NotImplemented


class Entity(BaseDomainModel):
    id: UUID4 = Field(default_factory=uuid4, allow_mutation=False)

    class Config(BaseDomainModel.Config):
        ...

    def __eq__(self, other: Any):
        if isinstance(other, type(self)):
            return self.id == other.id
        return NotImplemented

    def __hash__(self):  # type: ignore
        return hash(self.id)


class Aggregate(Entity):
    class Config(Entity.Config):
        ...
