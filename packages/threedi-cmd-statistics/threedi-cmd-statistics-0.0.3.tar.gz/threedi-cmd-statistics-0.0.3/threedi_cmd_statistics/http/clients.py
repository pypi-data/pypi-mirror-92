from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Dict
from functools import lru_cache
from openapi_client.api.statuses_api import StatusesApi
from openapi_client.api.contracts_api import ContractsApi
from openapi_client.api.usage_api import UsageApi
from openapi_client.aio.api_client import ApiClient


@dataclass
class AsyncClients:
    config: Dict

    @asynccontextmanager
    async def contracts(self):
        api_client = ApiClient(self.config)
        contracts_client = ContractsApi(api_client)
        yield contracts_client
        await api_client.close()

    @asynccontextmanager
    async def statuses(self):
        api_client = ApiClient(self.config)
        status_client = StatusesApi(api_client)
        yield status_client
        await api_client.close()

    @asynccontextmanager
    async def usage(self):
        api_client = ApiClient(self.config)
        usage_client = UsageApi(api_client)
        yield usage_client
        await api_client.close()


@lru_cache()
def async_api_clients(config):
    return AsyncClients(config)
