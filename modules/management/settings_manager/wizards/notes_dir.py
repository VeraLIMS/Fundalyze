"""Wizard to set the notes directory location."""

import os

from modules.config_utils import load_env, save_env

LABEL = "Notes Directory"


def run_wizard() -> None:
    print("\n=== Notes Directory Setup ===")
    env = load_env()
    current = env.get("NOTES_DIR", "notes")
    path = input(f"Notes directory [{current}]: ").strip() or current
    env["NOTES_DIR"] = path
    save_env(env)
    print(f"Notes directory saved to config/.env as '{path}'.\n")
