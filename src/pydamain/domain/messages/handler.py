from typing import Any, Iterable, Protocol, TypeVar


F_contra = TypeVar("F_contra", contravariant=True)
R_co = TypeVar("R_co", covariant=True)


class UnknownHandler(Protocol[F_contra, R_co]):
    __name__: str

    async def __call__(self, _msg: F_contra, **kwds: Any) -> R_co:
        ...


Handler = UnknownHandler[F_contra, R_co]
Handlers = Iterable[Handler[F_contra, R_co]]
