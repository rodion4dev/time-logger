"""Набор команд для консольного приложения."""
from pathlib import Path

import typer

from time_logger import service, __project_name__ as project_name

_application = typer.Typer()


def run():
    _application(prog_name=project_name)


@_application.callback()
def check_application_directory(context: typer.Context):
    skip_check_for = remove_application_data.__name__.replace("_", "-")
    if context.invoked_subcommand == skip_check_for:
        return

    service.check_application_directory()


@_application.command(short_help=service.log_start.__doc__)
def log_start(task: str, start_time: str = None):
    try:
        service.log_start(task, start_time=start_time)
    except service.ServiceError as error:
        typer.echo(message=str(error))
        raise typer.Exit(code=1)


@_application.command(short_help=service.log_stop.__doc__)
def log_stop(task: str, stop_time: str = None):
    try:
        service.log_stop(task, stop_time=stop_time)
    except service.ServiceError as error:
        typer.echo(message=str(error))
        raise typer.Exit(code=1)


@_application.command(short_help=service.calculate_time.__doc__)
def calculate_time(task: str):
    try:
        hours, minutes = service.calculate_time(task)
        typer.echo(message=f"Затраченное время \n--> Часов: {hours}, минут: {minutes}")
    except service.ServiceError as error:
        typer.echo(message=str(error))
        raise typer.Exit(code=1)


@_application.command(short_help=service.remove_application_data.__doc__)
def remove_application_data():
    try:
        service.remove_application_data()
    except service.ServiceError as error:
        typer.echo(message=str(error))
        raise typer.Exit(code=1)


@_application.command(short_help=service.import_database.__doc__)
def import_database(database: Path):
    service.import_database(database)
    typer.echo(message="Готово!")
