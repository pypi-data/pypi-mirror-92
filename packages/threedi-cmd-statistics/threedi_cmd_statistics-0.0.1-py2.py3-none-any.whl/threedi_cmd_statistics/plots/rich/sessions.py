from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from rich.style import Style
from rich.padding import Padding
from rich.table import Table

from threedi_cmd_statistics.console import console
from threedi_cmd_statistics.commands.models import MonthsChoices

from typing import List
from openapi_client.models import SimulationStatusStatistics


@dataclass
class SessionCount:
    result: List[SimulationStatusStatistics]
    crashed: int = field(init=False)
    finished: int = field(init=False)
    total: int = field(init=False)
    percentage_crashed: int = field(init=False)
    percentage_finished: int = field(init=False)

    def __post_init__(self):
        for stat in self.result:
            setattr(self, stat.name, stat.total)

        if not hasattr(self, "crashed"):
            self.crashed = 0
        if not hasattr(self, "finished"):
            self.finished = 0
        self.total = self.crashed + self.finished
        try:
            self.percentage_crashed = round((self.crashed * 100) / self.total)
        except ZeroDivisionError:
            self.percentage_crashed = 0
        try:
            self.percentage_finished = round(
                (self.finished * 100) / self.total
            )
        except ZeroDivisionError:
            self.percentage_finished = 0


class SessionCountGrids:
    def __init__(
        self,
        session_count: SessionCount,
    ):
        self.session_count = session_count
        self.name_column_width = int((console.width * 6) / 100)
        self.count_column_width = int((console.width * 5) / 100)
        self.perc_column_width = int((console.width * 5) / 100)
        self.width_left = (console.width * 84) / 100
        self.crashed_style = Style(bgcolor="red")
        self.finished_style = Style(bgcolor="green")

    def _get_base_grid(self) -> Table:
        grid = Table.grid(expand=False)
        grid.add_column(width=self.name_column_width)
        grid.add_column(
            width=self.count_column_width,
            style=Style(color="magenta", bold=True),
            justify="right",
        )
        grid.add_column(
            width=self.perc_column_width,
            style=Style(color="magenta", bold=True),
        )
        return grid

    @property
    def finished_grid(self) -> Table:
        grid = self._get_base_grid()
        plot_column_width = int(
            (self.width_left * self.session_count.percentage_finished) / 100
        )
        grid.add_column(
            max_width=plot_column_width,
            width=plot_column_width,
            style=self.finished_style,
        )
        grid.add_row(
            "finished",
            f"{self.session_count.finished}",
            f" [{self.session_count.percentage_finished}%]",
            "",
        )
        return grid

    @property
    def crashed_grid(self) -> Table:
        grid = self._get_base_grid()
        plot_column_width = int(
            (self.width_left * self.session_count.percentage_crashed) / 100
        )
        grid.add_column(
            max_width=plot_column_width,
            width=plot_column_width,
            style=self.crashed_style,
        )
        grid.add_row(
            "crashed",
            f"{self.session_count.crashed}",
            f" [{self.session_count.percentage_crashed}%]",
            "",
        )
        return grid


def plot_sessions(
    result: List[SimulationStatusStatistics],
    month: Optional[MonthsChoices],
    year: Optional[str],
    dates: Optional[List[datetime]],
    user_filter: Optional[str],
    organisation_filter: Optional[str],
    record: bool = False,
) -> None:
    if record:
        console.record = True
    session_count = SessionCount(result)
    grids = SessionCountGrids(session_count)
    plot_sessions_params(month, year, dates, user_filter, organisation_filter)
    console.print(Padding("", (1, 0)))
    title = f"[bold italic blue]Total {session_count.total}"
    console.print(title)
    console.print(grids.crashed_grid)
    console.print(grids.finished_grid)
    console.print(Padding("", (1, 0)))


def plot_sessions_params(
    month: Optional[MonthsChoices],
    year: Optional[str],
    dates: Optional[List[datetime]],
    user_filter: Optional[str],
    organisation_filter: Optional[str],
):
    base_str = f"[bold] Session count"
    if month:
        base_str += f" | {month.name}"
    if year:
        base_str += f" | {year}"
    if dates:
        try:
            start_date, end_date = dates
            base_str += f" {start_date} - {end_date}"
        except ValueError:
            base_str += f" since {dates[0]}"
    if user_filter:
        base_str += f" | user {user_filter}"
    if organisation_filter:
        base_str += f" | organisation {organisation_filter}"
    console.rule(f"{base_str}")
