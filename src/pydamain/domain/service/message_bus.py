import asyncio
from typing import (
    Any,
    Optional,
    Awaitable,
    Callable,
    Literal,
    TypeVar,
    overload,
)

from ..messages.base import Message, MessageCatchContext, get_issued_messages

from .handler import Handler

M = TypeVar("M", bound=Message)
R = TypeVar("R")
Handlers = tuple[Handler[M, R], ...]


Hook = Callable[[M, Handler[M, R]], Awaitable[None]]


async def handle(
    message: M,
    handler: Handler[M, Any],
    deps: dict[str, Any],
    pre_hook: Optional[Hook[M, Any]] = None,
    post_hook: Optional[Hook[M, Any]] = None,
):
    if pre_hook:
        await pre_hook(message, handler)
    result = await handler(message, **deps)
    if post_hook:
        await post_hook(message, handler)
    return result


async def handle_parallel(
    message: M,
    handlers: tuple[Handler[M, Any], ...],
    deps: dict[str, Any],
    pre_hook: Optional[Hook[M, Any]] = None,
    post_hook: Optional[Hook[M, Any]] = None,
):
    coros = (
        handle(message, handler, deps, pre_hook, post_hook) for handler in handlers
    )
    return await asyncio.gather(*coros, return_exceptions=True)


class MessageBus:
    def __init__(
        self,
        *,
        deps: dict[str, Any],
        pre_hook: Optional[Hook[Message, Any]] = None,
        post_hook: Optional[Hook[Message, Any]] = None,
    ) -> None:
        self._deps: dict[str, Any] = deps
        self._handler_map: dict[
            type[Message], Handler[Message, Any] | Handlers[Message, Any]
        ] = {}
        self._pre_hook = pre_hook
        self._post_hook = post_hook

    def register(
        self, message_type: type[M], handler: Handler[M, Any] | Handlers[M, Any]
    ):
        self._handler_map[message_type] = handler

    @overload
    async def dispatch(self, message: Message) -> Any:
        ...

    @overload
    async def dispatch(
        self, message: Message, return_hooked_task: Literal[True] = True
    ) -> tuple[Any, asyncio.Future[list[Any]]]:
        ...

    async def dispatch(self, message: Message, return_hooked_task: bool = False):
        result, hooked = await asyncio.create_task(self._dispatch(message))
        coros = (self._dispatch(msg) for msg in hooked)
        hooked_task = asyncio.gather(*coros, return_exceptions=True)
        if return_hooked_task:
            return result, hooked_task
        await hooked_task
        return result

    async def _dispatch(self, message: Message):
        with MessageCatchContext():
            handler = self._handler_map[type(message)]
            if isinstance(handler, tuple):
                result = await handle_parallel(
                    message, handler, self._deps, self._pre_hook, self._post_hook
                )
            else:
                result = await handle(
                    message, handler, self._deps, self._pre_hook, self._post_hook
                )
            messages = get_issued_messages()
        return result, messages
