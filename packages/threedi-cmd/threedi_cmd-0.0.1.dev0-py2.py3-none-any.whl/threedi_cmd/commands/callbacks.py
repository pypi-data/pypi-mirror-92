import typer

from threedi_cmd.commands.settings import (
    Settings,
    EndpointOption,
    get_settings,
)
from threedi_cmd.commands.models import EndpointChoices


def api_callback(
        ctx: typer.Context,
        endpoint: EndpointChoices = typer.Option(
            EndpointChoices.production, case_sensitive=False
        ),

):
    if ctx.invoked_subcommand == 'auth':
        return
    endpoint_name = EndpointOption[endpoint.value].name
    settings = get_settings(endpoint_name)
    ctx.obj = settings
    ctx.call_on_close(Settings.save_settings)