"""Interactive manager for `config/settings.json` and `.env`."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

from modules.interface import (
    print_invalid_choice,
    print_header,
    input_or_cancel,
    print_menu,
)

import importlib

from modules.config_utils import CONFIG_DIR, load_env, load_settings, save_env, save_settings


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
    """Prompt for a key/value pair, returning empty strings if canceled."""
    key = input("Key (or press Enter to cancel): ").strip()
    if not key:
        return "", ""
    value = input("Value: ").strip()
    return key, value


def _show_dict(data: Dict[str, str]) -> None:
    """Pretty-print a simple key/value mapping."""
    if not data:
        print("(empty)")
    else:
        for k, v in data.items():
            print(f"{k} = {v}")


def _show_api_keys() -> None:
    """Display known API keys/tokens from the environment."""
    env = load_env()
    keys = {k: v for k, v in env.items() if any(tok in k.upper() for tok in ["KEY", "TOKEN"])}
    _show_dict(keys)


def _set_setting() -> None:
    """Prompt for and save a value in ``settings.json``."""
    key, val = _prompt_kv()
    if not key:
        print("Canceled.\n")
        return
    data = load_settings()
    data[key] = val
    save_settings(data)
    print("Saved setting.\n")


def _del_setting() -> None:
    """Delete a key from ``settings.json`` if it exists."""
    key = input_or_cancel("Key to delete")
    if not key:
        print("Canceled.\n")
        return
    data = load_settings()
    if key in data:
        data.pop(key)
        save_settings(data)
        print("Deleted.\n")
    else:
        print("Key not found.\n")


def _set_env_var() -> None:
    """Add or update an environment variable in ``config/.env``."""
    key, val = _prompt_kv()
    if not key:
        print("Canceled.\n")
        return
    env = load_env()
    env[key] = val
    save_env(env)
    print("Saved variable.\n")


def _del_env_var() -> None:
    """Remove a variable from ``config/.env`` if present."""
    key = input_or_cancel("Variable to delete")
    if not key:
        print("Canceled.\n")
        return
    env = load_env()
    if key in env:
        env.pop(key)
        save_env(env)
        print("Deleted.\n")
    else:
        print("Key not found.\n")

def _general_settings_menu() -> None:
    """Interactive submenu for managing ``settings.json``."""
    while True:
        print_header("\u2699\ufe0f General Settings")
        options = [
            "View settings.json",
            "Set Setting",
            "Delete Setting",
            "Return to Settings Menu",
        ]
        print_menu(options)
        choice = input(f"Select an option [1-{len(options)}]: ").strip()
        if choice == "1":
            _show_dict(load_settings())
        elif choice == "2":
            _set_setting()
        elif choice == "3":
            _del_setting()
        elif choice == "4":
            break
        else:
            print_invalid_choice()


def _env_menu() -> None:
    """Interactive submenu for editing ``config/.env``."""
    while True:
        print_header("\u2699\ufe0f Environment (.env)")
        options = [
            "View .env",
            "Set .env Variable",
            "Delete .env Variable",
            "Return to Settings Menu",
        ]
        print_menu(options)
        choice = input(f"Select an option [1-{len(options)}]: ").strip()
        if choice == "1":
            _show_dict(load_env())
        elif choice == "2":
            _set_env_var()
        elif choice == "3":
            _del_env_var()
        elif choice == "4":
            break
        else:
            print_invalid_choice()


def _wizards_menu() -> None:
    """Display available setup wizards and run the selected one."""
    wiz_map = {label: func for label, func in _discover_wizards()}
    default_order = [
        "Directus Connection",
        "OpenBB API Token",
        "FMP API Key",
        "OpenAI API Key",
        "Quick Setup",
        "Notes Directory",
        "Output Directory",
        "Timezone",
    ]
    order = [label for label in default_order if label in wiz_map]
    order.extend([lbl for lbl in wiz_map if lbl not in order])
    while True:
        print_header("\u2699\ufe0f Setup Wizards")
        options = [f"Setup {lbl}" for lbl in order]
        options.append("Return to Settings Menu")
        print_menu(options)
        choice = input(f"Select an option [1-{len(options)}]: ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(order)+1):
            print_invalid_choice()
            continue
        idx = int(choice)
        if idx == len(options):
            break
        label = order[idx-1]
        func = wiz_map.get(label)
        if func:
            func()
        else:
            print("Wizard not available.\n")


def run_settings_manager() -> None:
    """Interactive menu to edit configuration and run setup wizards."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    while True:
        print_header("\u2699\ufe0f Settings")
        options = [
            ("General Settings", _general_settings_menu),
            ("Environment (.env)", _env_menu),
            ("Setup Wizards", _wizards_menu),
            ("API Keys", _show_api_keys),
            ("Return to Main Menu", None),
        ]
        print_menu([lbl for lbl, _ in options])
        choice = input(f"Select an option [1-{len(options)}]: ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(options)):
            print_invalid_choice()
            continue
        idx = int(choice) - 1
        _, action = options[idx]
        if action is None:
            break
        action()
