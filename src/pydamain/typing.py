from typing import *  # type: ignore


_T_contra = TypeVar("_T_contra", contravariant=True)
_T_co = TypeVar("_T_co", covariant=True)


class _SyncHandler0(Protocol[_T_contra, _T_co]):
    __name__: str

    def __call__(self, __m: _T_contra, /, **kwargs: Any) -> _T_co:
        ...


class _SyncHandler1(Protocol[_T_contra, _T_co]):
    __name__: str

    def __call__(
        self, __m: _T_contra, /, __arg_1: Any, **kwargs: Any
    ) -> _T_co:
        ...


class _SyncHandler2(Protocol[_T_contra, _T_co]):
    __name__: str

    def __call__(
        self, __m: _T_contra, /, __arg_1: Any, __arg_2: Any, **kwargs: Any
    ) -> _T_co:
        ...


class _SyncHandler3(Protocol[_T_contra, _T_co]):
    __name__: str

    def __call__(
        self,
        __m: _T_contra,
        /,
        __arg_1: Any,
        __arg_2: Any,
        __arg_3: Any,
        **kwargs: Any,
    ) -> _T_co:
        ...


class _SyncHandler4(Protocol[_T_contra, _T_co]):
    __name__: str

    def __call__(
        self,
        __m: _T_contra,
        /,
        __arg_1: Any,
        __arg_2: Any,
        __arg_3: Any,
        __arg_4: Any,
        **kwargs: Any,
    ) -> _T_co:
        ...


class _SyncHandler5(Protocol[_T_contra, _T_co]):
    __name__: str

    def __call__(
        self,
        __m: _T_contra,
        /,
        __arg_1: Any,
        __arg_2: Any,
        __arg_3: Any,
        __arg_4: Any,
        __arg_5: Any,
        **kwargs: Any,
    ) -> _T_co:
        ...


class _SyncHandler6(Protocol[_T_contra, _T_co]):
    __name__: str

    def __call__(
        self,
        __m: _T_contra,
        /,
        __arg_1: Any,
        __arg_2: Any,
        __arg_3: Any,
        __arg_4: Any,
        __arg_5: Any,
        __arg_6: Any,
        **kwargs: Any,
    ) -> _T_co:
        ...


class _SyncHandler7(Protocol[_T_contra, _T_co]):
    __name__: str

    def __call__(
        self,
        __m: _T_contra,
        /,
        __arg_1: Any,
        __arg_2: Any,
        __arg_3: Any,
        __arg_4: Any,
        __arg_5: Any,
        __arg_6: Any,
        __arg_7: Any,
        **kwargs: Any,
    ) -> _T_co:
        ...


class _SyncHandler8(Protocol[_T_contra, _T_co]):
    __name__: str

    def __call__(
        self,
        __m: _T_contra,
        /,
        __arg_1: Any,
        __arg_2: Any,
        __arg_3: Any,
        __arg_4: Any,
        __arg_5: Any,
        __arg_6: Any,
        __arg_7: Any,
        __arg_8: Any,
        **kwargs: Any,
    ) -> _T_co:
        ...


class _SyncHandler9(Protocol[_T_contra, _T_co]):
    __name__: str

    def __call__(
        self,
        __m: _T_contra,
        /,
        __arg_1: Any,
        __arg_2: Any,
        __arg_3: Any,
        __arg_4: Any,
        __arg_5: Any,
        __arg_6: Any,
        __arg_7: Any,
        __arg_8: Any,
        __arg_9: Any,
        **kwargs: Any,
    ) -> _T_co:
        ...


class _SyncHandler10(Protocol[_T_contra, _T_co]):
    __name__: str

    def __call__(
        self,
        __m: _T_contra,
        /,
        __arg_1: Any,
        __arg_2: Any,
        __arg_3: Any,
        __arg_4: Any,
        __arg_5: Any,
        __arg_6: Any,
        __arg_7: Any,
        __arg_8: Any,
        __arg_9: Any,
        __arg_10: Any,
        **kwargs: Any,
    ) -> _T_co:
        ...


SyncHandler = (
    _SyncHandler0[_T_contra, _T_co]
    | _SyncHandler1[_T_contra, _T_co]
    | _SyncHandler2[_T_contra, _T_co]
    | _SyncHandler3[_T_contra, _T_co]
    | _SyncHandler4[_T_contra, _T_co]
    | _SyncHandler5[_T_contra, _T_co]
    | _SyncHandler6[_T_contra, _T_co]
    | _SyncHandler7[_T_contra, _T_co]
    | _SyncHandler8[_T_contra, _T_co]
    | _SyncHandler9[_T_contra, _T_co]
    | _SyncHandler10[_T_contra, _T_co]
)


class _AsyncHandler0(Protocol[_T_contra, _T_co]):
    __name__: str

    async def __call__(self, __m: _T_contra, /, **kwargs: Any) -> _T_co:
        ...


class _AsyncHandler1(Protocol[_T_contra, _T_co]):
    __name__: str

    async def __call__(
        self, __m: _T_contra, /, __arg_1: Any, **kwargs: Any
    ) -> _T_co:
        ...


class _AsyncHandler2(Protocol[_T_contra, _T_co]):
    __name__: str

    async def __call__(
        self, __m: _T_contra, /, __arg_1: Any, __arg_2: Any, **kwargs: Any
    ) -> _T_co:
        ...


class _AsyncHandler3(Protocol[_T_contra, _T_co]):
    __name__: str

    async def __call__(
        self,
        __m: _T_contra,
        /,
        __arg_1: Any,
        __arg_2: Any,
        __arg_3: Any,
        **kwargs: Any,
    ) -> _T_co:
        ...


class _AsyncHandler4(Protocol[_T_contra, _T_co]):
    __name__: str

    async def __call__(
        self,
        __m: _T_contra,
        /,
        __arg_1: Any,
        __arg_2: Any,
        __arg_3: Any,
        __arg_4: Any,
        **kwargs: Any,
    ) -> _T_co:
        ...


class _AsyncHandler5(Protocol[_T_contra, _T_co]):
    __name__: str

    async def __call__(
        self,
        __m: _T_contra,
        /,
        __arg_1: Any,
        __arg_2: Any,
        __arg_3: Any,
        __arg_4: Any,
        __arg_5: Any,
        **kwargs: Any,
    ) -> _T_co:
        ...


class _AsyncHandler6(Protocol[_T_contra, _T_co]):
    __name__: str

    async def __call__(
        self,
        __m: _T_contra,
        /,
        __arg_1: Any,
        __arg_2: Any,
        __arg_3: Any,
        __arg_4: Any,
        __arg_5: Any,
        __arg_6: Any,
        **kwargs: Any,
    ) -> _T_co:
        ...


class _AsyncHandler7(Protocol[_T_contra, _T_co]):
    __name__: str

    async def __call__(
        self,
        __m: _T_contra,
        /,
        __arg_1: Any,
        __arg_2: Any,
        __arg_3: Any,
        __arg_4: Any,
        __arg_5: Any,
        __arg_6: Any,
        __arg_7: Any,
        **kwargs: Any,
    ) -> _T_co:
        ...


class _AsyncHandler8(Protocol[_T_contra, _T_co]):
    __name__: str

    async def __call__(
        self,
        __m: _T_contra,
        /,
        __arg_1: Any,
        __arg_2: Any,
        __arg_3: Any,
        __arg_4: Any,
        __arg_5: Any,
        __arg_6: Any,
        __arg_7: Any,
        __arg_8: Any,
        **kwargs: Any,
    ) -> _T_co:
        ...


class _AsyncHandler9(Protocol[_T_contra, _T_co]):
    __name__: str

    async def __call__(
        self,
        __m: _T_contra,
        /,
        __arg_1: Any,
        __arg_2: Any,
        __arg_3: Any,
        __arg_4: Any,
        __arg_5: Any,
        __arg_6: Any,
        __arg_7: Any,
        __arg_8: Any,
        __arg_9: Any,
        **kwargs: Any,
    ) -> _T_co:
        ...


class _AsyncHandler10(Protocol[_T_contra, _T_co]):
    __name__: str

    async def __call__(
        self,
        __m: _T_contra,
        /,
        __arg_1: Any,
        __arg_2: Any,
        __arg_3: Any,
        __arg_4: Any,
        __arg_5: Any,
        __arg_6: Any,
        __arg_7: Any,
        __arg_8: Any,
        __arg_9: Any,
        __arg_10: Any,
        **kwargs: Any,
    ) -> _T_co:
        ...


AsyncHandler = (
    _AsyncHandler0[_T_contra, _T_co]
    | _AsyncHandler1[_T_contra, _T_co]
    | _AsyncHandler2[_T_contra, _T_co]
    | _AsyncHandler3[_T_contra, _T_co]
    | _AsyncHandler4[_T_contra, _T_co]
    | _AsyncHandler5[_T_contra, _T_co]
    | _AsyncHandler6[_T_contra, _T_co]
    | _AsyncHandler7[_T_contra, _T_co]
    | _AsyncHandler8[_T_contra, _T_co]
    | _AsyncHandler9[_T_contra, _T_co]
    | _AsyncHandler10[_T_contra, _T_co]
)


Handler = AsyncHandler[_T_contra, _T_co] | SyncHandler[_T_contra, _T_co]
