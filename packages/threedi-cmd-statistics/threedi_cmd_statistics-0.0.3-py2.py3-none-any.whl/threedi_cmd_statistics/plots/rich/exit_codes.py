from typing import Mapping
from functools import cached_property
from rich.table import Table
from rich import box

from threedi_cmd_statistics.statistics.models import simulation_crashed_exit_codes
from threedi_cmd_statistics.console import console


class ExitCodeTable:
    def __init__(self, exit_codes: Mapping[int, int]):
        self.exit_codes = exit_codes
        self.total = sum(exit_codes.values())

    @cached_property
    def _table(self) -> Table:
        table = Table(
            title="[bold red] ~ Crashed details ~",
            show_header=True,
            box=box.HORIZONTALS,
            show_lines=False,
            expand=True,
        )
        table.add_column("Exit Code", width=5)
        table.add_column(
            "Description",
            width=20,
            justify="left",
            style="magenta bold",
            header_style="magenta bold",
        )
        table.add_column(
            "Count",
            width=5,
            justify="left",
            style="bold cyan",
            header_style="bold cyan",
        )
        table.add_column(
            "Percentage",
            width=5,
            justify="left",
        )
        return table

    @cached_property
    def table(self) -> Table:
        for k, v in self.exit_codes.most_common():
            if description := simulation_crashed_exit_codes.get(k):
                if k is None:
                    k = "?"
                perc = round((v * 100) / self.total)
                self._table.add_row(
                    f"{k}",
                    f"{description}",
                    f"{v}",
                    f"{perc}",
                )
        return self._table


def plot_exit_codes(exit_codes: Mapping[int, int]):
    t = ExitCodeTable(exit_codes)
    console.print(t.table)
