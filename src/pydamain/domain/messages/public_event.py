from dataclasses import dataclass, field
from typing import Any, ClassVar, Optional, Protocol
from typing_extensions import dataclass_transform

from .event import Event


class _Dumper(Protocol):
    def dumps(self, obj: Any) -> bytes:
        ...


Dumper = _Dumper


@dataclass(frozen=True, kw_only=True, slots=True)
class PublicEvent(Event):

    DUMPER: ClassVar[Dumper]

    @property
    def from_(self) -> Optional[bytes]:
        return None

    def dumps_(self) -> bytes:
        return self.DUMPER.dumps(self)


@dataclass_transform(
    eq_default=True,
    order_default=False,
    kw_only_default=True,
    field_descriptors=(field,),
)
def public_event(cls: type[PublicEvent]):  # type: ignore
    assert issubclass(cls, PublicEvent)
    return dataclass(cls, frozen=True, kw_only=True, slots=True)  # type: ignore
