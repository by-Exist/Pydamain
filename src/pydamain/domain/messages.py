import asyncio
from contextvars import ContextVar
from dataclasses import dataclass
from typing import (
    Any,
    Awaitable,
    ClassVar,
    Iterable,
    Protocol,
    TypeVar,
    cast,
)
from typing_extensions import Self, dataclass_transform  # type: ignore


# ============================================================================
# Typing
# ============================================================================
M = TypeVar("M", contravariant=True)
R = TypeVar("R", covariant=True)


class SyncHandler(Protocol[M, R]):
    __name__: str

    def __call__(self, _msg: M, *args: Any, **kwds: Any) -> R:
        ...


class AsyncHandler(Protocol[M, R]):
    __name__: str

    def __call__(self, _msg: M, *args: Any, **kwds: Any) -> Awaitable[R]:
        ...


UnknownHandler = AsyncHandler[M, R] | SyncHandler[M, R]


# ============================================================================
# Handle Function
# ============================================================================
async def handle(
    msg: M, handler: UnknownHandler[M, R], deps: dict[str, Any]
) -> R:
    """
    핸들러 함수에 첫번째 인자와 종속성을 주입하여 처리할 때 사용되는 함수입니다.

    handler가
    - Async일 경우 await으로 처리됩니다.
    - Sync일 경우 asyncio.to_thread로 처리됩니다.
    """
    if asyncio.iscoroutinefunction(handler):
        handler = cast(AsyncHandler[M, R], handler)
        return await handler(msg, **deps)
    handler = cast(SyncHandler[M, R], handler)
    return await asyncio.to_thread(handler, msg, **deps)


# ============================================================================
# Event
# ============================================================================
E = TypeVar("E", bound="Event")
Handlers = Iterable[UnknownHandler[E, Any]]


# TODO: handle에 return_coroutine을 bool로 받아서, 발생한 이벤트의 처리 코루틴을 반환해버리면?
# response 이후 처리하도록 할 수도 있지 않을까?
class Event:
    """
    ## [ Event ]
    이벤트 클래스를 정의하는데에 사용되는 믹스인 클래스입니다.

    사용자는 일반적으로 다음과 같이 자신의 이벤트 클래스를 정의합니다.

    ```python
    @event
    class ExampleEvent(Event):
        ...
    ```

    Event 클래스의 대략적인 구조는 다음과 같습니다.

    ```python
    class Event:
        # self를 처리하는데에 사용될 Callable들입니다.
        handlers: ClassVar[Handlers[Self]] = {...}

        # Self.handlers를 활용해 self를 별도의 Task에서 처리합니다.
        # 종료 전, self의 처리 과정에서 issue된 이벤트를 모아 재귀적으로 handle합니다.
        async def handle(self): ...

        # self를 처리하기 직전 수행됩니다.
        async def pre_handle(self): ...

        # self를 처리한 직후 수행됩니다.
        async def post_handle(self): ...

        # 이벤트를 발행합니다.
        # command.handle 또는 event.handle의 처리 중 발생한 이벤트가 아니라면
        # LookupError 예외가 발생합니다.
        async def issue(self): ...
    ```

    Event 클래스를 커스텀하여 훅 메서드를 재정의할 수 있습니다.

    ```python
    class CustomEvent(Event):
        async def pre_handle(self): ...
        async def post_handle(self): ...

    @event
    class ExampleEvent(CustomEvent): ...
    ```
    """

    handlers: ClassVar[Handlers["Event"]] = None  # type: ignore

    def __init_subclass__(cls) -> None:
        cls.handlers = set(cls.handlers)

    def issue(self):
        event_list = events_context_var.get()
        event_list.append(self)

    async def pre_handle(self):
        ...

    async def post_handle(self):
        ...

    async def handle(self, deps: dict[str, Any]):
        await self.pre_handle()
        events = await asyncio.create_task(self._handle(deps))
        await self.post_handle()
        await handle_events(events, deps, ignore_exception=True)

    async def _handle(self, deps: dict[str, Any]):
        if not self.handlers:
            return list[Event]()
        with EventCatcher() as event_catcher:
            await asyncio.gather(
                *(handle(self, handler, deps) for handler in self.handlers),
                return_exceptions=True,
            )
        return event_catcher.events


@dataclass_transform(kw_only_default=True)
def event(cls: type[Any]):
    """
    ## [ event ]
    이벤트 클래스를 정의하는데에 사용될 데코레이터입니다.
    값 객체와 유사합니다.

    (cls) -> dataclass(frozen=True, kw_only=True, slots=True)(cls)

    사용자가 이벤트를 정의하는 방식은 다음과 같습니다.

    ```python
    @event
    class ExampleEvent(Event):
        handlers : ClassVar[Handlers[Self]] = {...}
    ```
    Event을 상속받지 않을 경우 타입 에러가 발생합니다.

    ## [ Handlers ]
    이벤트 처리에 사용될 Callable들의 구조를 제약하는데에 활용됩니다.

    Iterable[Callable[[T, *_, **_], Any]] 형태를 강제합니다.
    """
    config = dict(
        init=True,
        repr=True,
        eq=True,
        order=False,
        unsafe_hash=False,
        frozen=True,  # Fixed
        match_args=True,
        kw_only=True,  # Fixed
        slots=True,  # Fixed
    )
    if not issubclass(cls, Event):
        raise TypeError(f"클래스 {cls.__name__}은(는) Event를 상속받아야 합니다.")
    return dataclass(**config)(cls)


async def handle_events(
    events: Iterable[Event],
    deps: dict[str, Any],
    ignore_exception: bool = True,
):
    coros = (event.handle(deps) for event in events)  # type: ignore
    await asyncio.gather(*coros, return_exceptions=ignore_exception)


# ============================================================================
# Command
# ============================================================================
C = TypeVar("C", bound="Command")
Handler = UnknownHandler[C, Any]


class Command:
    """
    ## [ Command ]
    커맨드 클래스를 정의하는데에 사용되는 믹스인 클래스입니다.

    사용자는 일반적으로 다음과 같이 자신의 커맨드 클래스를 정의합니다.

    ```python
    @command
    class ExampleCommand(Command):
        ...
    ```

    Command 클래스의 대략적인 구조는 다음과 같습니다.

    ```python
    class Command:
        # self를 처리하는데에 사용될 Callable입니다.
        handler: ClassVar[Handler[Self]] = {...}

        # Self.handler를 활용해 self를 별도의 Task에서 처리합니다.
        # 종료 전, self의 처리 과정에서 issue된 이벤트를 모아 재귀적으로 handle합니다.
        async def handle(self): ...

        # self를 처리하기 직전 수행됩니다.
        async def pre_handle(self): ...

        # self를 처리한 직후 수행됩니다.
        async def post_handle(self): ...
    ```

    Command 클래스를 커스텀하여 훅 메서드를 재정의할 수 있습니다.

    ```python
    class CustomCommand(Command):
        async def pre_handle(self): ...
        async def post_handle(self): ...

    @command
    class ExampleCommand(CustomCommand): ...
    ```
    """

    handler: ClassVar[Handler["Command"]] = None  # type: ignore

    async def pre_handle(self):
        ...

    async def post_handle(self):
        ...

    async def handle(self, deps: dict[str, Any]):
        await self.pre_handle()
        events = await asyncio.create_task(self._handle(deps))
        await self.post_handle()
        await handle_events(events, deps, ignore_exception=True)

    async def _handle(self, deps: dict[str, Any]):
        if not self.handler:
            return list[Event]()
        with EventCatcher() as event_catcher:
            await handle(self, self.handler, deps)
        return event_catcher.events


@dataclass_transform(kw_only_default=True)
def command(cls: type[Any]):
    """
    ## [ command ]
    커맨드 클래스를 정의하는데에 사용될 데코레이터입니다.
    값 객체와 유사합니다.

    (cls) -> dataclass(frozen=True, kw_only=True, slots=True)(cls)

    사용자가 커맨드를 정의하는 방식은 다음과 같습니다.

    ```python
    @command
    class ExampleCommand(Command):
        handler : ClassVar[Handler[Self]] = ...
    ```

    Command를 상속받지 않을 경우 타입 에러가 발생합니다.

    ## [ Handler ]

    커맨드 처리에 사용될 Callable의 구조를 제약하는데에 활용됩니다.
    Callable[[T, *_, **_], Any] 형태를 강제합니다.
    """
    config = dict(
        init=True,
        repr=True,
        eq=True,
        order=False,
        unsafe_hash=False,
        frozen=True,  # Fixed
        match_args=True,
        kw_only=True,  # Fixed
        slots=True,  # Fixed
    )
    if not issubclass(cls, Command):
        raise TypeError(f"클래스 {cls.__name__}은(는) Command를 상속받아야 합니다.")
    return dataclass(**config)(cls)


# ============================================================================
# Event Catcher
# ============================================================================
events_context_var: ContextVar[list[Event]] = ContextVar("events_context_var")


class EventCatcher:
    def __init__(self):
        self.events: list[Event] = []

    def __enter__(self):
        self.token = events_context_var.set(list())
        return self

    def __exit__(self, *args: tuple[Any]):
        self.events.extend(events_context_var.get())
        events_context_var.reset(self.token)
