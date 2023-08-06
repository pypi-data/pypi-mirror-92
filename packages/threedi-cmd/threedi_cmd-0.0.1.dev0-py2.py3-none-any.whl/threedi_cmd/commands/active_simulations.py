import asyncio
from datetime import datetime
from enum import Enum
import typer

from threedi_cmd.console import console
from threedi_cmd.models.monitor import ActiveSimulations

from threedi_cmd.commands.settings import (
    Settings,
    EndpointOption,
    get_settings,
)


class EndpointChoices(str, Enum):
    localhost = "localhost"
    staging = "staging"
    production = "production"


active_sims_app = typer.Typer()


async def monitor_active_simulations(endpoint: str) -> None:
    """
    executes ActiveSimlations "run_monitor" task in the background
    """
    active_simulations = ActiveSimulations(endpoint)
    result = await asyncio.gather(
        active_simulations.run_monitor(), return_exceptions=True
    )
    if result:
        console.print(result, style="error")


@active_sims_app.command()
def simulations(
        ctx: typer.Context,
        endpoint: EndpointChoices = typer.Option(
            EndpointChoices.production, case_sensitive=False
        )
):
    """
    Show currently running simulations
    """
    endpoint = EndpointOption[endpoint.value].name
    settings = get_settings(endpoint)
    ctx.obj = settings
    ctx.call_on_close(Settings.save_settings)
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    try:
        console.print(f"[{start_time}] Starting active simulations worker")
        asyncio.run(monitor_active_simulations(endpoint))
    except KeyboardInterrupt:
        pass
    finally:
        console.print(
            f":sparkles: Bye bye, hope to see you soon! :sparkles:",
            style="success",
        )


if __name__ == '__main__':
    active_sims_app()
