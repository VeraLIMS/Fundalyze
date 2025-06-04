"""Interactive manager for `config/settings.json` and `.env`."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from modules.config_utils import CONFIG_DIR, ENV_PATH, SETTINGS_PATH, load_env, load_settings, save_env, save_settings


def _prompt_kv() -> tuple[str, str]:
    key = input("Key: ").strip()
    value = input("Value: ").strip()
    return key, value


def run_settings_manager() -> None:
    """Simple CLI to view and edit configuration files."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    while True:
        print("\n=== Settings Manager ===")
        print("1) View settings.json")
        print("2) Set setting")
        print("3) Delete setting")
        print("4) View .env")
        print("5) Set .env variable")
        print("6) Delete .env variable")
        print("7) Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            data = load_settings()
            if not data:
                print("(empty)")
            else:
                for k, v in data.items():
                    print(f"{k} = {v}")

        elif choice == "2":
            key, val = _prompt_kv()
            data = load_settings()
            data[key] = val
            save_settings(data)
            print("Saved setting.\n")

        elif choice == "3":
            key = input("Key to delete: ").strip()
            data = load_settings()
            if key in data:
                data.pop(key)
                save_settings(data)
                print("Deleted.\n")
            else:
                print("Key not found.\n")

        elif choice == "4":
            env = load_env()
            if not env:
                print("(empty)")
            else:
                for k, v in env.items():
                    print(f"{k}={v}")

        elif choice == "5":
            key, val = _prompt_kv()
            env = load_env()
            env[key] = val
            save_env(env)
            print("Saved variable.\n")

        elif choice == "6":
            key = input("Variable to delete: ").strip()
            env = load_env()
            if key in env:
                env.pop(key)
                save_env(env)
                print("Deleted.\n")
            else:
                print("Key not found.\n")

        elif choice == "7":
            break
        else:
            print("Invalid choice.\n")
