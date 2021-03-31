"""Набор настроек для проекта."""
from pathlib import Path

BASE_DIRECTORY = Path(__file__).resolve().parent.parent
TIME_FORMAT = "%H:%M"
DATABASE = BASE_DIRECTORY / "database.json"
