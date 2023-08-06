from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from functools import cached_property
from typing import Optional, List, Dict
from pathlib import Path
from openapi_client.models import UsageStatistics


SESSION_CNT_DEFS = "crashed,finished,initialized"


@dataclass
class UsageStatisticsResults:
    all: UsageStatistics
    live: UsageStatistics
    api: UsageStatistics

    def as_list(self):
        return [self.all, self.live, self.api]

    def as_dict(self):
        return asdict(self)


simulation_crashed_exit_codes = {
    # error
    4161: "simulation status starting for longer than 10 minutes with attached docker container",
    4262: "simulation status crashed for longer than 10 minutes with attached docker container",
    4263: "simulation status initialized, but no simulation container was found",
    4264: "simulation status postprocessing, but no simulation container was found",
    4265: "simulation status ended, but no simulation container was found",
    4120: "initial condition worker failed",
    4220: "event worker failed",
    4150: "ignition startup container failed",
    4240: "calculation crashed",
    4230: "scheduler requesting an API resource failed",
    4231: "uploading a file failed",
    4232: "unfinished tasks during shutdown",
    # timeout
    2150: "bringing up the simulation container timed out",
    2110: "simulation was initialized (thus never started)",
    2210: "paused timeout reached (default 5 min)",
    2120: "initial condition worker",
    2220: "event condition worker",
    2230: "adding action collection to queue",
    2240: "clear stale event data",
    None: "exit code unknown"
}
