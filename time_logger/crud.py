"""Модуль для CRUD операций."""
import json
from functools import wraps
from typing import TYPE_CHECKING

from time_logger.settings import DATABASE

if TYPE_CHECKING:
    from typing import Callable, Any


def _check_database(wrapping_function: "Callable") -> "Callable":
    @wraps(wrapping_function)
    def wrap(*args, **kwargs) -> "Any":
        if not DATABASE.exists():
            with DATABASE.open(mode="w") as database_descriptor:
                json.dump({}, database_descriptor)
        return wrapping_function(*args, **kwargs)

    return wrap


@_check_database
def read_data() -> dict:
    """Чтение данных из базы."""
    with DATABASE.open(mode="r") as database_descriptor:
        return json.load(database_descriptor)


def update_data(data: dict):
    """Обновление данных в базе на указанные."""
    with DATABASE.open(mode="w") as database_descriptor:
        json.dump(data, database_descriptor, indent=3)
