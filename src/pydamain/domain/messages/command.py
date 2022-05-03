from dataclasses import dataclass, field
from typing import Any, ClassVar, Protocol, TypeVar

from typing_extensions import Self, dataclass_transform

from .base import Message


M_contra = TypeVar("M_contra", contravariant=True)


class _CommandHandler(Protocol[M_contra]):

    __name__: str

    async def __call__(self, _msg: M_contra, **_: Any) -> Any:
        ...


C = TypeVar("C", bound="Command")
CommandHandler = _CommandHandler[C]


@dataclass(frozen=True, kw_only=True, slots=True)
class Command(Message):

    handler_: ClassVar[CommandHandler[Self]]

    async def _pre_handle(self, handler: CommandHandler[Self]):
        ...

    async def _post_handle(self, handler: CommandHandler[Self]):
        ...

    async def handle_(self, deps: dict[str, Any]) -> Any:
        handler = type(self).handler_
        await self._pre_handle(handler)
        result = await handler(self, **deps)
        await self._post_handle(handler)
        return result


@dataclass_transform(
    eq_default=True,
    order_default=False,
    kw_only_default=True,
    field_descriptors=(field,),
)
def command(cls: type[Command]):  # type: ignore
    assert issubclass(cls, Command)
    return dataclass(cls, frozen=True, kw_only=True, slots=True)  # type: ignore
