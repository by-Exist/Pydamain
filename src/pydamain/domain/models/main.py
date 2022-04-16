from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Generic, TypeVar
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
EntityID = TypeVar("EntityID")


@dataclass(eq=False, kw_only=True, slots=True)
class Entity(Generic[EntityID]):
    @property
    @abstractmethod
    def id(self) -> EntityID:
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
class Aggregate(Entity[EntityID]):
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
