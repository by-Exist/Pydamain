from dataclasses import dataclass, field

from typing_extensions import dataclass_transform

from .entity import Entity


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
