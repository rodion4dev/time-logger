"""Набор настроек для проекта."""
import os
from pathlib import Path

import typer

from time_logger import __project_name__ as application

_environment_directory = os.getenv(application.upper() + "_DIRECTORY")
if _environment_directory:
    APPLICATION_DATA = Path(_environment_directory).resolve()
else:
    APPLICATION_DATA = Path(typer.get_app_dir(application)).resolve()
DATABASE = APPLICATION_DATA / "database.json"
TIME_FORMAT = "%H:%M"
BACKUP_FORMAT = "%Y-%m-%d-%H-%M-%S-%f-database-backup.json"
