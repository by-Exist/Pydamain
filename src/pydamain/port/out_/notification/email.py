from dataclasses import dataclass, field
from typing import Protocol, TypeVar


M_contra = TypeVar("M_contra", contravariant=True)


class Notification(Protocol[M_contra]):
    async def send(self, msg: M_contra):
        ...


@dataclass(slots=True)
class FakeNotification(Notification[M_contra]):
    """
    # Example

    ```python
    import asyncio


    class ExampleNotification(FakeNotification[str]):
        ...


    msg = "string message..."
    ex = ExampleNotification()
    asyncio.run(ex.send(msg))

    # msg_box: list
    assert ex.msg_box[0] == msg

    ```
    """

    msg_box: list[M_contra] = field(default_factory=list, init=False)

    async def send(self, msg: M_contra):
        self.msg_box.append(msg)
