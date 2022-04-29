from typing import Any
from pydamain.domain.models import entity, Entity, field
from uuid import UUID, uuid4


@entity
class Example(Entity):
    id: UUID = field(default_factory=uuid4)
    name: str

    @property
    def identity(self):
        return self.id


class TestValueObject:
    a1 = Example(name="a")
    a2 = Example(name="a")

    def test_entity_eq(self):
        assert Example.__eq__ is object.__eq__
        assert self.a1 != self.a2

    def test_entity_hash(self):
        assert Example.__hash__ is object.__hash__
        assert len({self.a1, self.a2}) == 2
