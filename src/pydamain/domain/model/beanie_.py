from beanie import Document

from pydamain.domain.model import base


class ValueObject(base.ValueObject):
    ...


class Entity(base.Entity):
    ...


class Aggregate(Document, Entity):  # type: ignore
    class Config(Document.Config, Entity.Config):  # type: ignore
        ...
