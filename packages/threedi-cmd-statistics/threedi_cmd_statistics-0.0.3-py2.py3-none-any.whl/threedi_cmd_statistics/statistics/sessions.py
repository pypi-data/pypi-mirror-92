import asyncio
from collections import Counter
from threedi_cmd_statistics.http.clients import async_api_clients
from typing import Optional, List

from openapi_client import ApiException
from openapi_client.models import SimulationStatus, SimulationStatusStatistics
from threedi_cmd_statistics.http.tools import calculate_pagination_offsets
from threedi_cmd_statistics.console import console

from openapi_client.api.statuses_api import StatusesApi
from threedi_cmd_statistics.statistics.tools import check_task_results, StatusMessages
from threedi_cmd_statistics.models import SessionsOptions

SESSION_CNT_DEFS = "crashed,finished,initialized"


EXCLUDE_EXIT_CODES = [2110, 2210, 4264]


def _get_exit_code_counter(results: List[SimulationStatus]):
    return Counter(
        [
            x.exit_code
            for x in results
            if x.exit_code not in EXCLUDE_EXIT_CODES
        ]
    )


def correct_count(
    status_results: List[List[SimulationStatusStatistics]],
) -> List[SimulationStatusStatistics]:
    stats = status_results.pop(0)
    for tr in status_results:
        if not tr:
            continue

        cnt = tr[0].total
        for stat in stats:
            if stat.name == "crashed":
                stat.total -= cnt
            elif stat.name == "finished":
                stat.total += cnt

    return stats


class Sessions:
    def __init__(
        self,
        options: SessionsOptions
    ):
        self.options = options

    async def get_crashed_details(self):
        base_kwargs = self.options.status_crashed_kwargs
        with console.status(StatusMessages.FETCH_STATUS_MESSAGE.value):
            clients = async_api_clients(self.options.settings.configuration)
            async with clients.statuses() as client:
                try:
                    resp = await client.statuses_list(**base_kwargs)
                except ApiException as err:
                    if self.options.verbose:
                        console.print_exception()
                    else:
                        console.print(f"{err}")
                        return []

                if not resp:
                    return []

                if not resp.next:
                    return _get_exit_code_counter(resp.results)

                offsets = calculate_pagination_offsets(resp.count)
                tasks = []
                for offset in offsets:
                    kwargs_copy = base_kwargs.copy()
                    kwargs_copy["offset"] = offset
                    fetch_task = asyncio.create_task(
                        client.statuses_list(**kwargs_copy)
                    )
                    tasks.append(fetch_task)
                task_results = await asyncio.gather(
                    *tasks, return_exceptions=True
                )
        console.log(StatusMessages.FETCHED.value)

        results = []
        for task_result in task_results:
            if isinstance(task_result, Exception):
                console.print(task_result, style="error")
                return []
            results.extend(task_result.results)
        return _get_exit_code_counter(results)

    async def get_statistics(
        self,
    ) -> Optional[List[SimulationStatusStatistics]]:
        all_tasks = []
        with console.status(StatusMessages.FETCH_STATUS_MESSAGE.value):
            clients = async_api_clients(self.options.settings.configuration)
            loop = asyncio.get_event_loop()
            async with clients.statuses() as client:
                stats_task = loop.create_task(
                    client.statuses_overview(**self.options.kwargs)
                )
                all_tasks.append(stats_task)
                extra_tasks = await self.get_exclude_exit_code_tasks(client)
                all_tasks.extend(extra_tasks)
                task_results = await asyncio.gather(
                    *all_tasks, return_exceptions=True
                )
        console.log(StatusMessages.FETCHED.value)
        if results := check_task_results(task_results, self.options.verbose):
            return correct_count(results)
        return []

    async def get_exclude_exit_code_tasks(
        self, client: StatusesApi
    ) -> List[asyncio.Task]:
        tasks = []
        for exit_code in EXCLUDE_EXIT_CODES:
            new_kwargs = self.options.kwargs.copy()
            new_kwargs["exit_code"] = exit_code
            t = asyncio.create_task(client.statuses_overview(**new_kwargs))
            tasks.append(t)
        return tasks
