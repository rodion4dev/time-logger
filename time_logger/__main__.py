"""
Точка входа в пакет из командной строки.

Использование:
python -m time_logger --help
"""
from time_logger import _cli

from time_logger import __name__ as project_name

_cli.application(prog_name=project_name)
