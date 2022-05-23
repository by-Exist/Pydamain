from pydamain.domain.models import Entity, field
from uuid import UUID, uuid4


class Example(Entity):
    _id: UUID = field(default_factory=uuid4)
    name: str

    @property
    def identity(self):
        return self._id


def test_entity_eq():
    some_id = uuid4()
    assert Example(_id=some_id, name="fdsa") != Example(_id=some_id, name="fdsa")
    assert Example.__eq__ == object.__eq__


def test_entity_hash():
    some_id = uuid4()
    assert (
        len({Example(_id=some_id, name="fdsa"), Example(_id=some_id, name="fdsa")}) == 2
    )
    assert Example.__hash__ == object.__hash__