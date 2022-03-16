from typing import Any
from uuid import uuid4

from pydantic import Field, UUID4

from .base import BaseDomainModel


class ValueObject(BaseDomainModel):
    class Config(BaseDomainModel.Config):
        allow_mutation = False

    def __eq__(self, other: Any):
        if isinstance(other, type(self)):
            return self.__dict__ == other.__dict__
        return NotImplemented


class Entity(BaseDomainModel):
    id: UUID4 = Field(
        default_factory=uuid4, exclude=True, allow_mutation=False
    )

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
