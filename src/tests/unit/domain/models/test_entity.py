from pydamain.domain.models import Entity, field
from uuid import UUID, uuid4


class Example(Entity):
    id: UUID = field(default_factory=uuid4)
    name: str

    @property
    def identity(self):
        return self.id
