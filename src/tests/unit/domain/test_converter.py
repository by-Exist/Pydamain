from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Any, Optional

from pydamain.domain.converter import converter


@unique
class ExEnum(Enum):
    ONE = 1
    TWO = 2


@dataclass
class ExDataclass:
    a: str = "a"


@dataclass
class Example:

    any_: Any = "any"

    int_: int = 1
    float_: float = 1.0
    str_: str = "..."
    bytes_: bytes = b"..."

    enum_: ExEnum = ExEnum.ONE

    option_: Optional[int] = None
    list_: list[Optional[int]] = field(default_factory=lambda: [1, 2, None])
    set_: set[Optional[int]] = field(default_factory=lambda: {1, 2, None})
    frozenset_: frozenset[Optional[int]] = frozenset([1, 2, None])
    dict_: dict[str, Optional[int]] = field(default_factory=lambda: {"key": None})
    tuple_: tuple[int, str] = (1, "fdsa")
    tuple__: tuple[Optional[int], ...] = (1, 2, None)

    dataclass_: ExDataclass = ExDataclass()


def test_convert():

    example = Example()
    dumps = converter.unstructure(example)  # type: ignore
    loads = converter.structure(dumps, Example)
    assert example == loads
