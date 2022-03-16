from typing import Any, Awaitable, Protocol, TypeVar


T_contra = TypeVar("T_contra", contravariant=True)
T_co = TypeVar("T_co", covariant=True)


class SyncHandler(Protocol[T_contra, T_co]):
    __name__: str

    def __call__(self, __msg: T_contra, /, **__kwg: Any) -> T_co:
        ...


class AsyncHandler(Protocol[T_contra, T_co]):
    __name__: str

    async def __call__(self, __msg: T_contra, /, **__kwg: Any) -> T_co:
        ...


class Handler(Protocol[T_contra, T_co]):
    __name__: str

    def __call__(
        self, __msg: T_contra, /, **__kwg: Any
    ) -> T_co | Awaitable[T_co]:
        ...
