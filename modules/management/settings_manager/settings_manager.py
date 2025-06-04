"""Interactive manager for `config/settings.json` and `.env`."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

import importlib

from modules.config_utils import CONFIG_DIR, ENV_PATH, SETTINGS_PATH, load_env, load_settings, save_env, save_settings


def _discover_wizards():
    """Return list of (label, callable) tuples for available wizard modules."""
    wizards = []
    wiz_dir = Path(__file__).resolve().parent / "wizards"
    if wiz_dir.exists():
        for py in sorted(wiz_dir.glob("*.py")):
            if py.name.startswith("_") or py.name == "__init__.py":
                continue
            module_name = f"{__package__}.wizards.{py.stem}"
            try:
                mod = importlib.import_module(module_name)
            except Exception:
                continue
            label = getattr(mod, "LABEL", py.stem)
            func = getattr(mod, "run_wizard", None)
            if callable(func):
                wizards.append((label, func))
    return wizards


def _prompt_kv() -> tuple[str, str]:
    key = input("Key: ").strip()
    value = input("Value: ").strip()
    return key, value


def _show_dict(data: Dict[str, str]) -> None:
    if not data:
        print("(empty)")
    else:
        for k, v in data.items():
            print(f"{k} = {v}")


def _set_setting() -> None:
    key, val = _prompt_kv()
    data = load_settings()
    data[key] = val
    save_settings(data)
    print("Saved setting.\n")


def _del_setting() -> None:
    key = input("Key to delete: ").strip()
    data = load_settings()
    if key in data:
        data.pop(key)
        save_settings(data)
        print("Deleted.\n")
    else:
        print("Key not found.\n")


def _set_env_var() -> None:
    key, val = _prompt_kv()
    env = load_env()
    env[key] = val
    save_env(env)
    print("Saved variable.\n")


def _del_env_var() -> None:
    key = input("Variable to delete: ").strip()
    env = load_env()
    if key in env:
        env.pop(key)
        save_env(env)
        print("Deleted.\n")
    else:
        print("Key not found.\n")


def run_settings_manager() -> None:
    """Interactive menu to edit configuration and run setup wizards."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    wizards = _discover_wizards()

    while True:
        print("\n=== Settings Manager ===")

        options: list[tuple[str, callable | None]] = [
            ("View settings.json", lambda: _show_dict(load_settings())),
            ("Set setting", _set_setting),
            ("Delete setting", _del_setting),
            ("View .env", lambda: _show_dict(load_env())),
            ("Set .env variable", _set_env_var),
            ("Delete .env variable", _del_env_var),
        ]

        # Append dynamic wizards
        for label, func in wizards:
            options.append((f"Run wizard: {label}", func))

        options.append(("Exit", None))

        for idx, (lbl, _) in enumerate(options, start=1):
            print(f"{idx}) {lbl}")

        choice = input("Enter choice: ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(options)):
            print("Invalid choice.\n")
            continue

        idx = int(choice) - 1
        _, action = options[idx]
        if action is None:
            break
        action()
