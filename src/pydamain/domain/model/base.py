import orjson
import typing

from pydantic import BaseModel


def orjson_dumps(v: typing.Any, *, default: typing.Any):
    return orjson.dumps(v, default).decode()


class BaseDomainModel(BaseModel):
    class Config(BaseModel.Config):
        validate_all = True
        allow_population_by_field_name = True
        validate_assignment = True
        orm_mode = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
