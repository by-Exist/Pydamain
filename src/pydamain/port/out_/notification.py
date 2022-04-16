from typing import Protocol, TypeVar


M_contra = TypeVar("M_contra", contravariant=True)


class Notification(Protocol[M_contra]):
    async def send(self, msg: M_contra):
        ...