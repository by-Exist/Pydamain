from datetime import datetime
from typing import Any
from uuid import uuid4
import orjson

from pydantic import BaseModel, Field, UUID4


def orjson_dumps(v: Any, *, default: Any):
    return orjson.dumps(v, default).decode()


class BaseMessage(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    create_time: datetime = Field(default_factory=datetime.now)

    class Config:
        validate_all = True
        allow_mutation = False
        allow_population_by_field_name = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
