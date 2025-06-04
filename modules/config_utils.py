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
