from functools import cached_property
from typing import List
from rich.table import Table
from rich import box

from threedi_cmd_statistics.console import console

UNLIMITED = [9999, 999]


class CustomerTable:
    def __init__(self, customers):
        self.customers = customers

    @cached_property
    def _table(self) -> Table:
        table = Table(
            show_header=True,
            box=box.HORIZONTALS,
            show_lines=False,
            expand=True,
        )
        table.add_column("Unique Id", width=25)
        table.add_column(
            "Name",
            width=20,
            justify="left",
            style="bold cyan",
            header_style="bold cyan",
        )
        table.add_column(
            "Hours Used",
            width=10,
            justify="left",
            style="magenta bold",
            header_style="magenta bold",
        )
        table.add_column(
            "Hours Bought",
            width=10,
            justify="left",
        )

        table.add_column(
            "Percentage Hours Used",
            width=20,
            justify="left",
        )
        return table

    @cached_property
    def customers_table(self) -> Table:

        for entry in self.customers:
            percentage = round((entry.hours_used * 100) / entry.hours_bought)
            if entry.hours_bought in UNLIMITED:
                entry.hours_bought = "[dim italic blue1]unlimited"
            if percentage == 0:
                p = f"[dim italic blue1]-"
            elif 1 <= percentage < 5:
                p = f"[bold green]{percentage}"
            elif 5 < percentage < 10:
                p = f"[bold light_goldenrod3]{percentage}"
            elif 10 < percentage < 50:
                p = f"[bold dark_orange]{percentage}"
            else:
                p = f"[bold red1]{percentage}"
            self._table.add_row(
                f"{entry.organisation}",
                f"{entry.organisation_name}",
                f"{entry.hours_used}",
                f"{entry.hours_bought}",
                f"{p}",
            )
        return self._table


def plot_customers(results: List, record: bool = False):

    ct = CustomerTable(results)
    if record:
        console.record = True
    console.print(ct.customers_table)
