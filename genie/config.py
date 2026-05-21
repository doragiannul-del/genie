from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

CONFIG_PATH = Path.home() / ".genie" / "config.toml"

_ERROR_MESSAGE = """No configuration found. Choose one of two approaches:

Option 1 — environment variables (via shell or .env file):
    API_KEY=...
    API_BASE_URL=...
    AI_MODEL=...

Option 2 — config file at ~/.genie/config.toml:
    [genie]
    api_key = "..."
    base_url = "..."
    ai_model = "..."
"""


@dataclass
class Config:
    api_key: str
    base_url: str
    model: str


def load_config() -> Config:
    load_dotenv()

    if os.environ.get("API_KEY"):
        return Config(
            api_key=os.environ["API_KEY"],
            base_url=os.environ["API_BASE_URL"],
            model=os.environ["AI_MODEL"],
        )

    if CONFIG_PATH.exists():
        with CONFIG_PATH.open("rb") as f:
            data = tomllib.load(f)
        genie = data.get("genie", {})
        if api_key := genie.get("api_key"):
            return Config(
                api_key=api_key,
                base_url=genie["base_url"],
                model=genie["ai_model"],
            )

    raise RuntimeError(_ERROR_MESSAGE)
