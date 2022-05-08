from dataclasses import dataclass, field
from typing import Any, ClassVar, TypeVar

from typing_extensions import Self, dataclass_transform

from .base import Message
from .typing_ import Handler


SelfCommand = TypeVar("SelfCommand", bound="Command")
CommandHandler = Handler[SelfCommand, Any]


@dataclass(frozen=True, kw_only=True, slots=True)
class Command(Message):

    HANDLER: ClassVar[CommandHandler[Self]]

    async def _pre_handle(self, handler: CommandHandler[Self]):
        ...

    async def _post_handle(self, handler: CommandHandler[Self]):
        ...

    async def handle_(self, deps: dict[str, Any]):
        handler = type(self).HANDLER
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
