import atexit
from datetime import datetime
from typing import List, Optional
from pathlib import Path

import typer
from cmd_client.commands.models import EndpointChoices
from cmd_client.commands.settings import (
    Settings,
    EndpointOption,
    get_settings,
)

from threedi_cmd_statistics.commands import exit_handler
from threedi_cmd_statistics.commands.models import MonthsChoices
from threedi_cmd_statistics.console import console
from threedi_cmd_statistics.validators import ValidationError
from threedi_cmd_statistics.validators.models import OptionsValidator
from threedi_cmd_statistics.models import SessionsOptions, UsageOptions


def html_callback(html_export_path: str):
    atexit.register(exit_handler, export_path=html_export_path)


HtmlExportPath = typer.Option(
    None,
    exists=False,
    dir_okay=True,
    writable=True,
    resolve_path=True,
    help="Export results to a html file.",
    callback=html_callback
)


def stats_callback(
    ctx: typer.Context,
    endpoint: EndpointChoices = typer.Option(
        EndpointChoices.production, case_sensitive=False
    ),
    month: MonthsChoices = typer.Option(
        None, help="month of the current year"
    ),
    year: str = typer.Option(None, help="sessions throughout the whole year"),
    date: Optional[List[datetime]] = typer.Option(
        None,
        help="sessions since the given date. "
             "Use a second date option to select a custom period of time. ",
    ),
    user_filter: str = typer.Option(None, help="filter by user name"),
    organisation_filter: str = typer.Option(
        None, help="filter by organisation uuid"
    ),
    html_export_path: Path = HtmlExportPath,
    verbose: bool = typer.Option(
        False,
        help="Show tracebacks and such",
    ),
):
    options_validator = OptionsValidator(
        month, year, date, user_filter, organisation_filter
    )
    try:
        options_validator.validate()
    except ValidationError as err:
        console.print(f"{err}", style="error")
        raise typer.Exit(1)
    endpoint_name = EndpointOption[endpoint.value].name
    settings = get_settings(endpoint_name)

    if ctx.invoked_subcommand == 'sessions':
        options = SessionsOptions(
            html_export_path, verbose, settings, month, year, date, user_filter, organisation_filter
        )
    elif ctx.invoked_subcommand == 'usage':
        options = UsageOptions(
            html_export_path, verbose, settings, month, year, date, user_filter, organisation_filter)
    else:
        return
    ctx.obj = options
    ctx.call_on_close(Settings.save_settings)


