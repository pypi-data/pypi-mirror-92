from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from functools import cached_property
from typing import Optional, List, Any
from pathlib import Path

from cmd_client.commands.settings import Settings

from threedi_cmd_statistics.http.tools import LIMIT
from threedi_cmd_statistics.console import console

SESSION_CNT_DEFS = "crashed,finished,initialized"


@dataclass
class BaseOptions:
    html_export_path: Path
    verbose: bool
    settings: Settings


@dataclass
class StatisticsOptions(BaseOptions):
    month: Optional[Enum]
    year: Optional[str]
    dates: Optional[List[datetime]]
    user_filter: Optional[str]
    organisation_filter: Optional[str]

    def save(self):
        try:
            self.settings.save()
        except Exception as err:
            console.print(f"Could noo save settings: {err}", style="warning")

    @cached_property
    def _status_base_kwargs(self):
        kwargs = {}
        if self.month:
            kwargs["created__month"] = self.month.value

        if self.year:
            kwargs["created__year"] = self.year

        if self.month and not self.year:
            kwargs["created__year"] = datetime.utcnow().year

        if self.dates:
            try:
                start_date, end_date = self.dates
                kwargs["created__gt"] = start_date
                kwargs["created__lt"] = end_date
            except ValueError:
                kwargs["created__gt"] = self.dates[0]
        if self.user_filter:
            kwargs["simulation__user__username"] = self.user_filter
        if self.organisation_filter:
            kwargs[
                "simulation__organisation__unique_id"
            ] = self.organisation_filter
        return kwargs

    @property
    def period(self):
        base_str = ""
        if self.dates:
            try:
                start_date, end_date = self.dates
                base_str += f" {start_date} - {end_date}"
            except ValueError:
                base_str += f" since {self.dates[0]}"
            return base_str

        if self.month and self.year:
            return f"{self.month.name} {self.year}"
        elif not self.month and self.year:
            return f"{self.year}"
        elif self.month and not self.year:
            return f"{self.month.name} {datetime.utcnow().year}"
        else:
            return "all"


@dataclass
class SessionsOptions(StatisticsOptions):

    @cached_property
    def kwargs(self):
        kwargs = {"name__in": SESSION_CNT_DEFS}
        base_kwargs = self._status_base_kwargs.copy()
        kwargs.update(base_kwargs)
        return kwargs

    @cached_property
    def status_crashed_kwargs(self):
        kwargs = {"name__in": "crashed", "limit": LIMIT}
        base_kwargs = self._status_base_kwargs.copy()
        kwargs.update(base_kwargs)
        return kwargs


@dataclass
class UsageOptions(StatisticsOptions):

    @cached_property
    def kwargs(self):
        kwargs = {}
        if self.month:
            kwargs["started__month"] = self.month.value
            kwargs["finished__month"] = self.month.value
        if self.year:
            kwargs["started__year"] = self.year
            kwargs["finished__year"] = self.year
        if self.dates:
            try:
                start_date, end_date = self.dates
                kwargs["started__gt"] = start_date
                kwargs["finished__lt"] = end_date
            except ValueError:
                kwargs["started__gt"] = self.dates[0]
        if self.user_filter:
            kwargs["simulation__user__username"] = self.user_filter
        if self.organisation_filter:
            kwargs[
                "simulation__organisation__unique_id"
            ] = self.organisation_filter
        return kwargs


@dataclass
class CustomerOptions(BaseOptions):
    all_customers: bool = False

    @cached_property
    def kwargs(self):
        kwargs = {"limit": LIMIT}
        if not self.all_customers:
            kwargs["hours_used__gt"] = 0
        return kwargs
