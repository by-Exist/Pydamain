from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from typing_extensions import dataclass_transform


# ============================================================================
# Entity
# ============================================================================
@dataclass(eq=False, kw_only=True, slots=True)
class Entity(metaclass=ABCMeta):
    @property
    @abstractmethod
    def identity(self) -> Any:
        ...


@dataclass_transform(
    eq_default=False,
    order_default=False,
    kw_only_default=True,
    field_descriptors=(field,),
)
def entity(cls: type[Entity]):  # type: ignore
    assert issubclass(cls, Entity)
    return dataclass(cls, eq=False, kw_only=True, slots=True)  # type: ignore
