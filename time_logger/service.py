"""Сервисный слой приложения."""
import json
from contextlib import suppress
from datetime import datetime
from functools import wraps
from shutil import rmtree
from typing import TYPE_CHECKING

from time_logger.crud import (
    DatabaseDataError,
    backup_data,
    read_data,
    read_task,
    update_data,
    update_task,
)
from time_logger.settings import APPLICATION_DATA, BACKUP_FORMAT
from time_logger.time import (
    calculate_interval,
    convert_minutes,
    extract_time,
    format_time,
)

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Optional, Callable, Any


class ServiceError(Exception):
    """Общая ошибка для сервисного слоя."""


def _check_lock(function) -> "Callable":
    @wraps(function)
    def wrap(*args, **kwargs) -> "Any":
        task = args[0]
        with suppress(DatabaseDataError):
            task_data = read_task(task)
            if task_data.get("is_locked"):
                raise ServiceError("Задача заблокирована для измененй.")
        return function(*args, **kwargs)

    return wrap


@_check_lock
def log_start(task: str, start_time: "Optional[str]"):
    """Запись о начале работы над задачей."""
    data: dict = read_data()
    if task not in data:
        data.update({task: {"records": [], "is_started": None, "is_locked": False}})

    is_started = data[task]["is_started"] and isinstance(data[task]["is_started"], bool)
    if is_started:
        raise ServiceError(f"Время начала работы над задачей {task} уже записано.")

    start_time = format_time(extract_time(start_time))
    data[task]["records"].append({"start_time": start_time, "stop_time": None})
    data[task]["is_started"] = True

    update_data(data)
    return start_time


def log_stop(task: str, stop_time: "Optional[str]"):
    """Запись об окончании работы над задачей."""
    data: dict = read_data()
    if not (task in data and data[task]["is_started"]):
        raise ServiceError(f"У задачи {task} отсутствует время начала.")

    if data[task]["records"][-1]["stop_time"]:
        raise ServiceError("Время работы над задачей уже записано.")

    stop_time = format_time(extract_time(stop_time))
    data[task]["records"][-1].update({"stop_time": stop_time})
    data[task]["is_started"] = False

    update_data(data)
    return data[task]["records"][-1]["start_time"], stop_time


def calculate_time(task: str):
    """Подсчёт затраченного времени на указанную задачу."""
    data: dict = read_data()
    if task not in data:
        raise ServiceError("Такой задачи не существует.")

    hours, minutes = 0, 0
    for record in data[task]["records"]:
        start_time, stop_time = record["start_time"], record["stop_time"]
        if not all([start_time, stop_time]):
            continue

        calculated_hours, calculated_minutes = calculate_interval(
            extract_time(start_time), extract_time(stop_time)
        )
        hours += calculated_hours
        minutes += calculated_minutes

    hours, minutes = convert_minutes(hours, minutes)
    return hours, minutes


def import_database(database: "Path"):
    """Импортирование указанной базы данных."""
    with database.open(mode="r") as database_descriptor:
        data = json.load(database_descriptor)

    update_data(data)


def remove_application_data():
    """Удаление директории приложения."""
    if not APPLICATION_DATA.exists():
        raise ServiceError("Директория приложения не найдена.")

    rmtree(APPLICATION_DATA)


def check_application_directory():
    """Проверка наличия директории приложения и создание в случае отсутствия."""
    if not APPLICATION_DATA.exists():
        APPLICATION_DATA.mkdir(mode=0o755)


def lock_task(task: str):
    """Блокировка указанной задачи для обновлений."""
    try:
        task_data = read_task(task)
    except DatabaseDataError as error:
        raise ServiceError(str(error)) from error

    if task_data.get("is_locked"):
        raise ServiceError("Задача уже заблокирована для изменений.")

    if len(task_data["records"]) == 0:
        task_data["is_locked"] = True
        update_task(task, task_data)
        return

    if not task_data["records"][-1]["stop_time"]:
        raise ServiceError(
            "Задача недоступна для блокировки: не записано время остановки."
        )

    task_data["is_locked"] = True
    update_task(task, task_data)


def unlock_task(task: str):
    """Разблокировка указанной задачи для изменений."""
    try:
        task_data = read_task(task)
    except DatabaseDataError as error:
        raise ServiceError(str(error)) from error

    is_locked = task_data.get("is_locked")
    if not is_locked:
        raise ServiceError("Задача не заблокирована.")

    if isinstance(is_locked, bool):
        task_data["is_locked"] = False
        update_task(task, task_data)


def backup_database() -> "Path":
    """Создание резервной копии базы данных."""
    backup = APPLICATION_DATA / datetime.now().strftime(BACKUP_FORMAT)
    backup_data(backup)
    return backup
