from dataclasses import dataclass, field

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