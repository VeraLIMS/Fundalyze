"""Wizard to configure and validate the OpenAI API key."""

import openai

from modules.config_utils import load_env, save_env

LABEL = "OpenAI API Key"


def run_wizard() -> None:
    print("\n=== OpenAI API Key Setup ===")
    key = input("Enter OpenAI API Key: ").strip()
    if not key:
        print("No key provided.\n")
        return

    openai.api_key = key
    try:
        openai.models.list()
    except Exception as e:
        print(f"Validation failed: {e}\n")
        return

    env = load_env()
    env["OPENAI_API_KEY"] = key
    save_env(env)
    print("API key saved to config/.env.\n")
