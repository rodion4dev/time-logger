"""Модуль для CRUD операций."""
import json
from functools import wraps
from typing import TYPE_CHECKING

from time_logger.settings import DATABASE

if TYPE_CHECKING:
    from typing import Callable, Any
    from pathlib import Path


class DatabaseDataError(Exception):
    pass


def _check_database(wrapping_function: "Callable") -> "Callable":
    @wraps(wrapping_function)
    def wrap(*args, **kwargs) -> "Any":
        if not DATABASE.exists():
            with DATABASE.open(mode="w") as database_descriptor:
                json.dump({}, database_descriptor)
        return wrapping_function(*args, **kwargs)

    return wrap


def _check_task(task: str):
    data = read_data()
    if task not in data:
        raise DatabaseDataError("Указанной задачи не существует.")
    return data


@_check_database
def read_task(task: str) -> dict:
    """Получение указанной задачи."""
    data = _check_task(task)
    return data[task]


@_check_database
def update_task(task: str, data: dict):
    """Обновление задачи переданными данными."""
    _check_task(task)
    all_data = read_data()
    all_data[task] = data
    update_data(all_data)


@_check_database
def read_data() -> dict:
    """Чтение данных из базы."""
    with DATABASE.open(mode="r") as database_descriptor:
        return json.load(database_descriptor)


def update_data(data: dict):
    """Обновление данных в базе на указанные."""
    with DATABASE.open(mode="w") as database_descriptor:
        json.dump(data, database_descriptor, indent=3)


@_check_database
def backup_data(backup: "Path"):
    """Создание резервной копии данных по указанному пути."""
    with DATABASE.open(mode="r") as database_descriptor:
        data = json.load(database_descriptor, indent=3)
    with backup.open(mode="w") as database_descriptor:
        json.dump(data, database_descriptor)
