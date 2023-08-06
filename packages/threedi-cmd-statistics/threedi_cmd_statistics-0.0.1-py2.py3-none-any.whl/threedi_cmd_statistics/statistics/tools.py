from enum import Enum
from typing import List, Optional

from threedi_cmd_statistics.console import console


class StatusMessages(str, Enum):
    FETCH_STATUS_MESSAGE = "[bold green] Fetching data from 3Di API..."
    FETCHED = "[bold green]:heavy_check_mark:[/bold green] Fetched data..."


def check_task_results(
    task_results: List, verbose: bool = False
) -> Optional[List]:
    results = []
    for task_result in task_results:
        if isinstance(task_result, Exception):
            if verbose:
                try:
                    raise task_result
                except:
                    console.print_exception()
            console.print(task_result, style="error")
            return
        if hasattr(task_result, "results"):
            results.extend(task_result.results)
        else:
            results.append(task_result)
        continue
    return results
