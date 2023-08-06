from cmd_client.plugins.models import AppMeta, AppRegistry
from threedi_cmd_statistics.commands.apps import statistics_app, customers_app

statistics_meta = AppMeta(
    app=statistics_app,
    name="statistics",
    help="3Di API statistics, like session counts etc",
    add_to="api"
)

customers_meta = AppMeta(
    app=customers_app,
    name="customers",
    help="List 3Di customers",
    add_to="api"
)

registry = AppRegistry(
    apps={
        inst.name: inst for inst in
        [statistics_meta, customers_meta]
    }
)
