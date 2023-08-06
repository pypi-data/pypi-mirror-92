"""Top-level package for threedi_api_stats."""

__author__ = """Lars Claussen"""
__email__ = "claussen.lars@nelen-schuurmans.nl"
__version__ = "0.1.1"

from threedi_cmd.plugins.models import AppRegistry

from functools import lru_cache


@lru_cache()
def get_apps() -> AppRegistry:
    from threedi_cmd_statistics.commands.app_definitions import registry
    return registry
