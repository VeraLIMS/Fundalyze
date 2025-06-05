"""Populate .env using existing environment variables."""

import os

from modules.config_utils import load_env, save_env

LABEL = "Quick Setup"


def run_wizard() -> None:
    print("\n=== Quick Setup ===")
    env = load_env()

    keys = [
        "OPENBB_TOKEN",
        "FMP_API_KEY",
        "OPENAI_API_KEY",
        "NOTES_DIR",
        "OUTPUT_DIR",
        "DIRECTUS_URL",
        "DIRECTUS_TOKEN",
        "DIRECTUS_PORTFOLIO_COLLECTION",
        "DIRECTUS_GROUPS_COLLECTION",
        "CF_ACCESS_CLIENT_ID",
        "CF_ACCESS_CLIENT_SECRET",
    ]

    found = False
    for key in keys:
        val = os.getenv(key)
        if val:
            env[key] = val
            found = True
    if found:
        save_env(env)
        print("Environment variables saved to config/.env.\n")
    else:
        print("No matching environment variables found.\n")

