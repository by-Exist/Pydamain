from datetime import date, time
from typing import Any
from uuid import UUID

from cattrs.preconf.orjson import make_converter


# ============================================================================
# Converter
# ============================================================================
# UUID
def unstructure_uuid(uuid: UUID):
    return uuid.hex


def structure_uuid(hex: str, _: Any):
    return UUID(hex)


# Date
def unstructure_date(date_: date):
    return date_.isoformat()


def structure_date(date_isoformat: str, _: Any):
    return date.fromisoformat(date_isoformat)


# Time
def unstructure_time(time_: time):
    return time_.isoformat()


def structure_time(time_isoformat: str, _: Any):
    return time.fromisoformat(time_isoformat)


converter = make_converter(forbid_extra_keys=True)

converter.register_unstructure_hook(UUID, unstructure_uuid)
converter.register_structure_hook(UUID, structure_uuid)

converter.register_unstructure_hook(date, unstructure_date)
converter.register_structure_hook(date, structure_date)

converter.register_unstructure_hook(time, unstructure_time)
converter.register_structure_hook(time, structure_time)
