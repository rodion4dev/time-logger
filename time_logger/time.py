"""Инструменты для работы с временем."""
from datetime import datetime, time
from time import strptime
from typing import TYPE_CHECKING

from time_logger.settings import TIME_FORMAT

if TYPE_CHECKING:
    from typing import Optional, Tuple


def extract_time(based_on: "Optional[str]") -> "time":
    """Парсинг указанного времени, опираясь на формат из настроек."""
    if based_on:
        parsed = strptime(based_on, TIME_FORMAT)
        return time(hour=parsed.tm_hour, minute=parsed.tm_min)
    else:
        now = datetime.now().time()
        return time(hour=now.hour, minute=now.minute)


def format_time(time_object: "time") -> str:
    """Форматирование времени по формату, указанному в настройках."""
    return time_object.strftime(TIME_FORMAT)


def calculate_interval(time_1: "time", time_2: "time") -> "Tuple[int, int]":
    """Подсчёт интервала между двумя объектами времени."""
    hours = abs(time_2.hour - time_1.hour)
    minutes = abs(time_2.minute - time_1.minute)
    return hours, minutes


def convert_minutes(hours: int, minutes: int) -> "Tuple[int, int]":
    """Конвертация переданных минут в значение указанных часов."""
    remainder = minutes % 60
    hours, minutes = int((minutes - remainder) / 60) + hours, remainder
    return hours, minutes
