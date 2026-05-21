from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

CONFIG_PATH = Path.home() / ".genie" / "config.toml"
DEFAULT_MODEL = "gemini-2.0-flash"

_ERROR_MESSAGE = """No configuration found. Choose one of two approaches:

Option 1 — environment variables (via shell or .env file):
    GEMINI_API_KEY=...
    GENIE_MODEL=gemini-2.0-flash   # optional, defaults to gemini-2.0-flash

Option 2 — config file at ~/.genie/config.toml:
    [genie]
    api_key = "..."
    model = "gemini-2.0-flash"     # optional, defaults to gemini-2.0-flash
"""


@dataclass
class Config:
    api_key: str
    model: str = DEFAULT_MODEL


def load_config() -> Config:
    load_dotenv()

    if os.environ.get("GEMINI_API_KEY"):
        return Config(
            api_key=os.environ["GEMINI_API_KEY"],
            model=os.environ.get("GENIE_MODEL", DEFAULT_MODEL),
        )

    if CONFIG_PATH.exists():
        with CONFIG_PATH.open("rb") as f:
            data = tomllib.load(f)
        genie = data.get("genie", {})
        if api_key := genie.get("api_key"):
            return Config(
                api_key=api_key,
                model=genie.get("model", DEFAULT_MODEL),
            )

    raise RuntimeError(_ERROR_MESSAGE)
