from typing import Any, ClassVar, TypeVar

from typing_extensions import Self

from .message import Message
from .typing_ import Handler


SelfCommand = TypeVar("SelfCommand", bound="Command")
CommandHandler = Handler[SelfCommand, Any]


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
