from typing import Protocol, TypeVar


T_contra = TypeVar("T_contra", contravariant=True)


class _Notification(Protocol[T_contra]):
    async def send(self, _msg: T_contra):
        ...


Message = TypeVar("Message")
Notification = _Notification[Message]
