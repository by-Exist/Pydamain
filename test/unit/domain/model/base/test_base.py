from dataclasses import dataclass
from datetime import datetime, date, time
from typing import Any, TypedDict
from uuid import UUID, uuid4
import pytest

from pydantic import ValidationError

from pydamain.domain.model.base import Field
from pydamain.domain.model.base import BaseDomainModel


class ValidationDefault(BaseDomainModel):

    test: int = Field(default="exception")


class ValidationDefaultFactory(BaseDomainModel):

    test: int = Field(default_factory=lambda: "exception")


class UseableAlias(BaseDomainModel):

    id: str = Field(alias="identity")


class OrmModeObject:
    def __init__(self, id: int):
        self.id = id


class OrmModeDomainModel(BaseDomainModel):

    id: int


@dataclass
class ExampleDataClass:
    value: str


class ExampleTypedDict(TypedDict):
    value: str


class NestedBaseDomainModel(BaseDomainModel):
    value: str


class JsonableTypes(BaseDomainModel):

    none_: None

    int_: int
    float_: float
    bool_: bool

    str_: str
    list_: list[Any]
    tuple_: tuple[Any, ...]
    set_: set[Any]
    frozenset_: frozenset[Any]

    dict_: dict[Any, Any]
    typeddict_: ExampleTypedDict

    datetime_: datetime
    date_: date
    time_: time

    uuid_: UUID

    dataclass_: ExampleDataClass

    nested: NestedBaseDomainModel


class TestBaseDomainModel:
    def test_validate_default_value(self):
        with pytest.raises(ValidationError):
            ValidationDefault()

    def test_validate_default_factory_value(self):
        with pytest.raises(ValidationError):
            ValidationDefaultFactory()

    def test_useable_alias(self):
        UseableAlias(identity="other")

    def test_on_orm_mode(self):
        omo = OrmModeObject(123)
        OrmModeDomainModel.from_orm(omo)

    def test_json_translation(self):
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
