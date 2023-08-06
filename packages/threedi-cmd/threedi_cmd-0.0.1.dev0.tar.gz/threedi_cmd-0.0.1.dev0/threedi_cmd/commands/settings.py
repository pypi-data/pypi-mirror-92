from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import timedelta
from datetime import datetime
from enum import Enum
from pathlib import Path
import sys
from urllib.parse import urlparse
from functools import lru_cache

import click
import jwt
import yaml
from rich.prompt import Prompt

from openapi_client import Configuration, ApiClient, ApiException
from threedi_api_client.threedi_api_client import ThreediApiClient
from threedi_api_client.aio.threedi_api_client import (
    ThreediApiClient as AsyncThreediApiClient,
)

from openapi_client.api.auth_api import AuthApi
from threedi_api_client.threedi_api_client import (
    is_token_usable,
    get_auth_token,
)

from threedi_cmd.console import console
from threedi_cmd.errors import ExitCodes

SCENARIO_DIR = Path(__file__).parent.parent / "scenarios"
REFRESH_TIME_DELTA = timedelta(hours=4).total_seconds()
EXPIRE_LEEWAY = -300


class EndpointOption(Enum):
    localhost = "http://localhost:8000/v3.0"
    staging = "https://api.staging.3di.live/v3.0"
    production = "https://api.3di.live/v3.0"


@lru_cache()
def get_settings(endpoint):
    return Settings(endpoint=endpoint)


@dataclass
class WebSocketSettings:
    api_base_url: str
    token: str
    host: str = field(init=False)
    proto: str = field(init=False)
    api_version: str = field(init=False)

    def __post_init__(self):
        parsed_url = urlparse(self.api_base_url)
        self.host = parsed_url.netloc
        self.proto = "wss" if parsed_url.scheme == "https" else "ws"
        self.api_version = parsed_url.path.lstrip("/")
        self.token = (
            self.token
            if self.token.startswith("Bearer")
            else f"Bearer {self.token}"
        )


@dataclass
class CachedConfig:
    username: str = ""
    access: str = ""
    refresh: str = ""
    organisation_uuid: str = ""
    result_folder: str = ""

    @classmethod
    def load_from_file(cls, file: Path) -> CachedConfig:
        """
        Loads saved settings from 3di_config.yaml. See save method for available attributes.
        """
        try:
            with open(file, "r") as f:
                cached_data = yaml.load(f, Loader=yaml.FullLoader)
                return cls(**cached_data)
        except OSError:
            # settings file does not yet exist
            return cls()


@dataclass
class ScenariosMeta:

    scenario_dir: Path = SCENARIO_DIR

    @property
    def scenarios(self):
        scenario_list = []
        scenario_files = self.scenario_dir.glob("*.yaml")
        for f in scenario_files:
            with f.open("r") as y:
                content = yaml.load_all(y, Loader=yaml.FullLoader)
                try:
                    meta = next(content)["meta"]
                    meta["file"] = f
                    scenario_list.append(meta)
                except KeyError:
                    raise AttributeError(
                        f"The scenario definition is missing the 'meta' section"
                    )
        return scenario_list


class Settings:
    """Settings that are saved (authentication) values between calls to the cli.

    The default settings are saved in the file '3di_config.yaml' which lives in
    the configuration folder of your operating system.
    """

    app_name = "3di-scenario"
    file_name = "3di_config.yaml"

    def __init__(self, endpoint: str = ""):
        self.endpoint = EndpointOption[endpoint].value
        self.cached_config = CachedConfig.load_from_file(self.config_file)
        self.refresh_api_key(self.configuration)
        self.websocket_settings = WebSocketSettings(
            api_base_url=self.endpoint, token=self.access
        )

    @property
    def username(self):
        return self.cached_config.username

    @property
    def access(self):
        return self.cached_config.access

    @property
    def refresh(self):
        return self.cached_config.refresh

    @property
    def organisation_uuid(self):
        return self.cached_config.organisation_uuid

    @property
    def result_folder(self):
        return self.cached_config.result_folder

    @property
    def app_dir(self) -> Path:
        _app_dir = Path(click.get_app_dir(app_name=self.app_name))
        _app_dir.mkdir(parents=True, exist_ok=True)
        return _app_dir

    @property
    def config_file(self) -> Path:
        return self.app_dir / self.file_name

    @property
    def configuration(self):
        configuration = Configuration(
            host=self.endpoint,
            username=f"{self.username}",
            api_key={
                "Authorization": f"{self.access}",
                "refresh": f"{self.refresh}",
            },
            api_key_prefix={"Authorization": "Bearer"},
        )
        configuration.refresh_api_key_hook = self.refresh_api_key
        return configuration

    @property
    def api_client(self) -> ThreediApiClient:
        client = ApiClient(self.configuration)
        return client

    @property
    def async_api_client(self) -> AsyncThreediApiClient:
        client = AsyncThreediApiClient(self.configuration)
        return client

    @property
    def scenarios(self):
        scenarios_meta = ScenariosMeta()
        return scenarios_meta.scenarios

    def save(self):
        with open(self.config_file, "w") as file:
            yaml.dump(
                asdict(self.cached_config),
                default_flow_style=False,
                stream=file,
            )

    @staticmethod
    def save_settings():
        ctx = click.get_current_context()
        ctx.obj.save()

    def do_refresh(self, token) -> bool:
        try:
            details = jwt.decode(
                token,
                options={"verify_signature": False},
                leeway=EXPIRE_LEEWAY,
            )
        except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.DecodeError):
            return True
        expiry_dt = datetime.fromtimestamp(details["exp"])
        sec_left = (expiry_dt - datetime.utcnow()).total_seconds()
        return sec_left <= REFRESH_TIME_DELTA

    def refresh_api_key(self, config: Configuration):
        """Refreshes the access key if its expired"""
        api_key = config.api_key.get("Authorization")
        if not self.do_refresh(api_key) and is_token_usable(api_key):
            return

        refresh_key = config.api_key.get("refresh")
        if is_token_usable(refresh_key):
            api_client = ApiClient(Configuration(config.host))
            auth = AuthApi(api_client)
            try:
                token = auth.auth_refresh_token_create(
                    {"refresh": config.api_key["refresh"]}
                )
                config.api_key = {"Authorization": token.access, "refresh": token.refresh}
                return
            except ApiException:
                self.credentials_prompt(config)
        else:
            self.credentials_prompt(config)

    def credentials_prompt(self, config: Configuration):
        console.rule(
            f":key: Authentication required for {config.host}",
            characters="*",
            style="gold3",
        )
        kwargs = {}
        try:
            if self.username:
                kwargs.update({"default": self.username})
        except AttributeError:
            pass
        username = Prompt.ask("Username", **kwargs)
        password = Prompt.ask("Password", password=True)

        try:
            token = get_auth_token(username, password, config.host)
        except ValueError as err:
            console.print(f":collision: {err}", style="error")
            sys.exit(ExitCodes.AUTHENTICATION_FAILED.value)

        # Update the settings
        self.cached_config.username = username
        self.cached_config.access = token.access
        self.cached_config.refresh = token.refresh
        config.api_key = {"Authorization": token.access, "refresh": token.refresh}
