from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing import Any
from typing_extensions import dataclass_transform


# ============================================================================
# Value Object
# ============================================================================
@dataclass(frozen=True, kw_only=True, slots=True)
class ValueObject:
    ...


@dataclass_transform(
    eq_default=True,
    order_default=False,
    kw_only_default=True,
    field_descriptors=(field,),
)
def value_object(cls: type[ValueObject]):  # type: ignore
    assert issubclass(cls, ValueObject)
    return dataclass(cls, frozen=True, kw_only=True, slots=True)  # type: ignore


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


# ============================================================================
# Aggregate
# ============================================================================
@dataclass(eq=False, kw_only=True, slots=True)
class Aggregate(Entity):
    ...


@dataclass_transform(
    eq_default=False,
    order_default=False,
    kw_only_default=True,
    field_descriptors=(field,),
)
def aggregate(cls: type[Aggregate]):  # type: ignore
    assert issubclass(cls, Aggregate)
    return dataclass(cls, eq=False, kw_only=True, slots=True)  # type: ignore
