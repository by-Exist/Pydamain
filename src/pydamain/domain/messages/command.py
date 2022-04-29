from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing import Any, ClassVar, TypeVar

from typing_extensions import Self, dataclass_transform

from ..handler import Handler


# ============================================================================
# Command
# ============================================================================
C = TypeVar("C", bound="Command")
CommandHandler = Handler[C, Any]


@dataclass(frozen=True, kw_only=True, slots=True)
class Command(metaclass=ABCMeta):

    handler: ClassVar[CommandHandler[Self] | None] = None

    @property
    @abstractmethod
    def identity(self) -> Any:
        ...


@dataclass_transform(
    eq_default=True,
    order_default=False,
    kw_only_default=True,
    field_descriptors=(field,),
)
def command(cls: type[Command]):  # type: ignore
    assert issubclass(cls, Command)
    return dataclass(cls, frozen=True, kw_only=True, slots=True)  # type: ignore
