from __future__ import annotations

from uuid import uuid4
import typing

from sqlmodel import Field, SQLModel, Relationship  # type: ignore
from pydantic import UUID4


class ValueObject(SQLModel):

    id: UUID4 = Field(default_factory=uuid4, primary_key=True, exclude=True)

    class Config(SQLModel.Config):
        validate_assigment = True


class Entity(SQLModel):

    id: UUID4 = Field(default_factory=uuid4, primary_key=True, exclude=True)

    class Config(SQLModel.Config):
        validate_assignment = True

    def __eq__(self, other: typing.Any):
        if isinstance(other, type(self)):
            return self.id == other.id
        return NotImplemented

    def __hash__(self):  # type: ignore
        return hash(self.id)


class Aggregate(Entity):

    version_number: int = Field(..., exclude=True)

    __mapper_args__: dict[str, typing.Any] = {"version_id_col": version_number}

    class Config(Entity.Config):
        ...
