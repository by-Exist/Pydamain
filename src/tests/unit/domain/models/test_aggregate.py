from typing import Any
from pydamain.domain.models import Aggregate, field
from uuid import UUID, uuid4


class Example(Aggregate):
    id: UUID = field(default_factory=uuid4)
    name: str

    @property
    def identity(self) -> Any:
        return self.id
