from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Any, TypedDict
from uuid import UUID, uuid4
import pytest

from pydantic import ValidationError

from pydamain.domain.model.base import BaseDomainModel, Field
from pydamain.domain.message.base import BaseMessage


@dataclass
class ExampleDataClass:
    value: str


class ExampleTypedDict(TypedDict):
    value: str


class NestedBaseDomainModel(BaseDomainModel):
    value: str


class JsonableTypes(BaseMessage):

    none_: None

    int_: int
    float_: float
    bool_: bool

    str_: str
    list_: list[Any]
    tuple_: tuple[Any, ...]
    set_: set[Any]
    frozenset_: frozenset[Any]

    datetime_: datetime
    date_: date
    time_: time

    uuid_: UUID

    dict_: dict[Any, Any]
    typeddict_: ExampleTypedDict
    dataclass_: ExampleDataClass
    nested: NestedBaseDomainModel


class ExampleBaseMessage(BaseMessage):
    value: str


class ValidationDefault(BaseMessage):
    value: str = Field(default=int)


class UseableAlias(BaseMessage):
    name: str = Field(alias="username")


class TestBaseMessage:
    def test_validate_default_value(self):
        with pytest.raises(ValidationError):
            ValidationDefault()

    def test_useable_alias(self):
        UseableAlias(username="other")

    def test_immutable(self):
        example = ExampleBaseMessage(value="immutable")
        with pytest.raises(TypeError):
            example.value = "change"

    def test_jsonable(self):
        origin = JsonableTypes(
            none_=None,
            int_=0,
            float_=0,
            bool_=True,
            str_="",
            list_=[],
            tuple_=tuple(),
            set_=set(),
            frozenset_=frozenset(),
            dict_={},
            typeddict_=ExampleTypedDict(value=""),
            datetime_=datetime.now(),
            date_=datetime.now().date(),
            time_=datetime.now().time(),
            uuid_=uuid4(),
            dataclass_=ExampleDataClass(""),
            nested=NestedBaseDomainModel(value="nested"),
        )
        json_string = origin.json()
        parsed = JsonableTypes.parse_raw(json_string)
        assert origin == parsed
