"""Набор команд для консольного приложения."""
import typer

from time_logger import service, __script_name__ as script

_application = typer.Typer(add_completion=False)


def run():
    _application(prog_name=script)


@_application.command(short_help="Создание записи о начале работы")
def log_start(task: str, start_time: str = None):
    try:
        service.log_start(task, start_time=start_time)
    except service.ServiceError as error:
        typer.echo(message=str(error))
        raise typer.Exit(code=1)


@_application.command(short_help="Создание записи об окончании работы")
def log_stop(task: str, stop_time: str = None):
    try:
        service.log_stop(task, stop_time=stop_time)
    except service.ServiceError as error:
        typer.echo(message=str(error))
        raise typer.Exit(code=1)


@_application.command(short_help="Подсчёт затраченного времени на задачу")
def calculate_time(task: str):
    try:
        hours, minutes = service.calculate_time(task)
        typer.echo(message=f"Затраченное время \n--> Часов: {hours}, минут: {minutes}")
    except service.ServiceError as error:
        typer.echo(message=str(error))
        raise typer.Exit(code=1)
