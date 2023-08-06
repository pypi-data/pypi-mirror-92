import asyncio
from concurrent.futures import CancelledError
from pathlib import Path
import typer

from threedi_cmd_statistics.statistics.customers import Customers
from threedi_cmd_statistics.statistics.sessions import Sessions
from threedi_cmd_statistics.plots.rich.sessions import (
    plot_sessions,
)
from threedi_cmd_statistics.plots.rich.exit_codes import plot_exit_codes
from threedi_cmd_statistics.plots.rich.customers import plot_customers

from threedi_cmd_statistics.commands.callbacks import HtmlExportPath
from threedi_cmd_statistics.console import console
from threedi_cmd_statistics.statistics.usage import Usage
from threedi_cmd_statistics.plots.rich.usage import (
    plot_usage,
)

from threedi_cmd_statistics.commands.callbacks import stats_callback

statistics_app = typer.Typer(callback=stats_callback)
customers_app = typer.Typer()


@statistics_app.command()
def sessions(
    ctx: typer.Context,
    show_crash_details: bool = typer.Option(
        False,
        "--crash-details",
        help="Show crash details",
    ),
):
    """default: all sessions since the beginning of mankind"""

    loop = asyncio.get_event_loop()
    record = bool(ctx.obj.html_export_path)
    sessions = Sessions(ctx.obj)
    tasks = [loop.create_task(sessions.get_statistics())]
    if show_crash_details:
        tasks.append(loop.create_task(sessions.get_crashed_details()))

    try:
        results = loop.run_until_complete(asyncio.gather(*tasks))
    except CancelledError:
        results = []
    finally:
        loop.stop()
    if not results or not results[0]:
        console.print("No sessions statistics found")
        raise typer.Exit(-1)
    plot_sessions(
        results[0], ctx.obj.month, ctx.obj.year, ctx.obj.dates, ctx.obj.user_filter, ctx.obj.organisation_filter, record
    )
    if show_crash_details and len(results) > 1:
        plot_exit_codes(results[1])


@statistics_app.command()
def usage(ctx: typer.Context):
    """
    Shows aggregated calculation time statistics, like the total, average or maximum calculation duration.
    Use the given options filters to narrow down the results to a given period of time of for specific user
    or organisation.

    To get the calculation statistics for December, 2020:

        $ usage --year 2020 --month 12

    Alternatively you can use several --date options to specify a custom period:

        $ usage --date 2020-2-22 --date 2020-12-24

    All these results will include the calculation time for all organisations you have
    the run_simulation permission for. To show the same statistics for a single organisation use
    the --organisation-filter

        $ usage --date 2020-2-22 --date 2020-12-24 --organisation-filter <uuid of the organisation>

    To further narrow down the results for a single user use the --user-filter

        $ usage --date 2020-2-22 --date 2020-12-24 --user-filter <user.name>

    """

    loop = asyncio.get_event_loop()
    record = bool(ctx.obj.html_export_path)
    usage = Usage(ctx.obj)
    try:
        results = loop.run_until_complete(usage.get_statistics())
    except CancelledError:
        results = None
    finally:
        loop.stop()
    if not results:
        base = ":confused: We're sorry but something went wrong."
        if not ctx.obj.verbose:
            base += "You can run this command again with the [bold red]--verbose[/bold red] option to get more information"  # noqa
        console.print(base)
        raise typer.Exit(1)
    plot_usage(results, ctx.obj.period, record)

from threedi_cmd_statistics.models import CustomerOptions


@customers_app.command()
def customers(
    ctx: typer.Context,
    all_customers: bool = typer.Option(
        False,
        "--all-customers",
        help="Show all customers (that is, not only active ones that have used some of their calucaltion plan",
    ),
    html_export_path: Path = HtmlExportPath,
    verbose: bool = typer.Option(
        False,
        help="Show tracebacks and such",
    ),
):
    """only available for admin/root user. The customer list is limited to active one by default.
    If you want to list all customers use the --all option."""
    loop = asyncio.get_event_loop()
    record = bool(html_export_path)
    options = CustomerOptions(html_export_path, verbose, ctx.obj, all_customers)
    customers = Customers(options)
    try:
        results = loop.run_until_complete(customers.get_statistics())
    except CancelledError:
        results = []
    finally:
        loop.stop()
    if not results:
        console.print(f"No customers found")
        raise typer.Exit(0)

    plot_customers(results, record)


if __name__ == "__main__":
    import typer
    from threedi_cmd_statistics.commands.app_definitions import registry

    main_app = typer.Typer()

    for app_name, app_meta in registry.apps.items():
        main_app.add_typer(app_meta.app, name=app_meta.name, help=app_meta.help)
    main_app()
