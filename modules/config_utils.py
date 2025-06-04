"""Utilities for loading environment variables and user settings."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv

# Directory containing config files
CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
ENV_PATH = CONFIG_DIR / ".env"
SETTINGS_PATH = CONFIG_DIR / "settings.json"

# Load environment variables from .env if present
if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)


def load_settings() -> Dict[str, Any]:
    """Return settings dictionary loaded from config/settings.json if it exists."""
    if SETTINGS_PATH.exists():
        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_settings(data: Dict[str, Any]) -> None:
    """Persist the provided settings dictionary to ``config/settings.json``."""
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_env() -> Dict[str, str]:
    """Return key-value pairs loaded from ``config/.env`` if it exists."""
    if not ENV_PATH.exists():
        return {}
    env: Dict[str, str] = {}
    for line in ENV_PATH.read_text().splitlines():
        if "=" in line:
            key, val = line.split("=", 1)
            env[key.strip()] = val.strip()
    return env


def save_env(env: Dict[str, str]) -> None:
    """Write key-value pairs to ``config/.env``."""
    ENV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(ENV_PATH, "w", encoding="utf-8") as f:
        for key, val in env.items():
            f.write(f"{key}={val}\n")
