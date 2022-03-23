from dataclasses import dataclass
from typing import Any
from typing_extensions import dataclass_transform


@dataclass_transform()
def value_object(cls: type[Any]):
    """
    값 객체 클래스를 정의하는데에 사용될 데코레이터입니다.

    (cls) -> dataclass(frozen=True, slots=True)(cls)

    사용자가 값 객체를 정의하는 방식은 다음과 같습니다.

    ```python
    @value_object
    class SomeValueObject:
        ...
    ```
    """
    config = dict(
        init=True,
        repr=True,
        eq=True,
        order=False,
        unsafe_hash=False,
        frozen=True,  # Fixed
        match_args=True,
        kw_only=False,
        slots=True,  # Fixed
    )
    return dataclass(**config)(cls)


@dataclass_transform()
def entity(cls: type[Any]):
    """
    엔티티 클래스를 정의하는데에 사용될 데코레이터입니다.

    (cls) -> dataclass(eq=False, slots=True)(cls)

    사용자가 엔티티를 정의하는 방식은 다음과 같습니다.

    ```python
    @entity
    class SomeEntity:
        # Entity identity
        _identity: UUID = field(default_factory=uuid4)

        # Hash
        def __hash__(self, other):
            return hash(self.id)
    ```

    Entity identity
    - 엔티티 식별자는 엔티티의 수명주기와 함께 하는 고유한 값입니다.
    - 식별자의 수정을 지양하기 위해 private 속성으로 정의하기를 권장합니다.

    Hash
    - 정의하지 않을 경우 object.__hash__가 사용되며 식별자의 개념과 어울리지 않는 동작입니다.
    """
    config = dict(
        init=True,
        repr=True,
        eq=False,  # Fixed
        order=False,
        unsafe_hash=False,
        frozen=False,
        match_args=True,
        kw_only=False,
        slots=True,  # Fixed
    )
    return dataclass(**config)(cls)


from uuid import UUID, uuid4
from dataclasses import field


@entity
class SubEntity:
    name: str
    _id: UUID = field(default_factory=uuid4)

    def __hash__(self) -> int:
        return hash(self._id)
