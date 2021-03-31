"""Сервисный слой приложения."""
from time_logger.crud import read_data, update_data
from time_logger.time import calculate_interval, extract_time, format_time


class ServiceError(Exception):
    """Общая ошибка для сервисного слоя."""


def log_start(task: str, start_time: str = None):
    """Запись о начале работы над задачей."""
    data: dict = read_data()
    if task not in data:
        data.update({task: {"records": [], "is_started": None}})

    is_started = data[task]["is_started"] and isinstance(data[task]["is_started"], bool)
    if is_started:
        raise ServiceError(f"Время для задачи {task} уже записано.")

    start_time = format_time(extract_time(start_time))
    data[task]["records"].append({"start_time": start_time, "stop_time": None})
    data[task]["is_started"] = True

    update_data(data)


def log_stop(task: str, stop_time: str = None):
    """Запись об окончании работы над задачей."""
    data: dict = read_data()
    if not (task in data and data[task]["is_started"]):
        raise ServiceError(f"У задачи {task} отсутствует время начала.")

    if data[task]["records"][-1]["stop_time"]:
        raise ServiceError("Время работы над задачей уже записано.")

    stop_time = format_time(extract_time(stop_time))
    data[task]["records"][-1].update({"stop_time": stop_time})

    update_data(data)


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
    return hours, minutes
