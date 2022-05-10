import asyncio
from typing import Any, Literal, overload

from ..messages.message import Message, MessageCatchContext


class MessageBus:
    def __init__(
        self,
        *,
        deps: dict[str, Any],
    ) -> None:
        self._deps: dict[str, Any] = deps

    @overload
    async def handle(
        self, message: Message, return_hooked_task: Literal[False] = False
    ) -> Any:
        ...

    @overload
    async def handle(
        self, message: Message, return_hooked_task: Literal[True] = True
    ) -> tuple[Any, asyncio.Future[list[Any]]]:
        ...

    async def handle(self, message: Message, return_hooked_task: bool = False):
        result, hooked = await asyncio.create_task(self._handle(message))
        coros = (self._handle(msg) for msg in hooked)
        hooked_task = asyncio.gather(*coros, return_exceptions=True)
        if return_hooked_task:
            return result, hooked_task
        await hooked_task
        return result

    async def _handle(self, message: Message):
        with MessageCatchContext() as message_catcher:
            result = await message.handle_(deps=self._deps)
        return result, message_catcher.messages
