from functools import cached_property
from rich.padding import Padding
from rich.table import Table
from rich import box

from threedi_cmd_statistics.console import console
from threedi_cmd_statistics.statistics.models import UsageStatisticsResults


def humanize_duration(secs: int):
    if not secs:
        return 0
    minutes, seconds = divmod(secs, 60)
    hours, minutes = divmod(minutes, 60)
    base_str = ""
    if hours >= 24:
        days, hours = divmod(hours, 24)
        base_str += f"{days:.0f} days "
        return f"{days:.0f} days hours {hours:.0f} minutes {minutes:.0f} and {seconds:.0f} seconds"
    if hours:
        base_str += f"{hours:.0f} hours "
    if minutes:
        base_str += f"{minutes:.0f} minutes "
    if seconds:
        base_str += f"and {seconds:.0f} seconds"
    return base_str
    # return f"{hours:.0f} hours {minutes:.0f} minutes and {seconds:.0f} seconds"


class UsageTable:
    def __init__(self, usage: UsageStatisticsResults, period):
        self.usage = usage
        self.period = period

    @cached_property
    def _table(self) -> Table:
        table = Table(
            title=f"[bold green] ~ {self.period} ~ ",
            show_header=True,
            box=box.HORIZONTALS,
            show_lines=False,
            expand=True,
        )
        table.add_column("Simulation Type", width=10)
        table.add_column(
            "Total sessions",
            width=10,
            justify="left",
            style="magenta bold",
            header_style="magenta bold",
        )
        table.add_column(
            "Total duration",
            width=20,
            justify="left",
            style="bold cyan",
            header_style="bold cyan",
        )
        table.add_column(
            "Average session duration",
            width=20,
            justify="left",
        )
        table.add_column(
            "Longest session duration",
            width=20,
            justify="left",
        )
        return table

    @cached_property
    def table(self) -> Table:
        for key, entry in self.usage.as_dict().items():
            self._table.add_row(
                f"{key}",
                f"{entry.total_sessions}",
                f"{humanize_duration(entry.total_duration)}",
                f"{humanize_duration(entry.avg_duration)}",
                f"{humanize_duration(entry.max_duration)}",
            )
        return self._table


def plot_usage(
    results: UsageStatisticsResults, period: str, record: bool = False
):

    us = UsageTable(results, period)
    if record:
        console.record = True
    console.print(Padding("", (1, 0)))
    console.print(us.table)
    console.print(Padding("", (1, 0)))
