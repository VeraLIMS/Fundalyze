"""Interactive manager for `config/settings.json` and `.env`."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

from modules.interface import print_invalid_choice

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
    key = input("Key: ").strip()
    value = input("Value: ").strip()
    return key, value


def _show_dict(data: Dict[str, str]) -> None:
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

def _general_settings_menu() -> None:
    while True:
        print("\n⚙️ General Settings")
        print("1) View settings.json")
        print("2) Set Setting")
        print("3) Delete Setting")
        print("4) Return to Settings Menu")
        choice = input("Select an option [1-4]: ").strip()
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
    while True:
        print("\n⚙️ Environment (.env)")
        print("1) View .env")
        print("2) Set .env Variable")
        print("3) Delete .env Variable")
        print("4) Return to Settings Menu")
        choice = input("Select an option [1-4]: ").strip()
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
        print("\n⚙️ Setup Wizards")
        for idx, lbl in enumerate(order, start=1):
            print(f"{idx}) Setup {lbl}")
        print(f"{len(order)+1}) Return to Settings Menu")
        choice = input(f"Select an option [1-{len(order)+1}]: ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(order)+1):
            print_invalid_choice()
            continue
        idx = int(choice)
        if idx == len(order)+1:
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
        print("\n⚙️ Settings")
        options = [
            ("General Settings", _general_settings_menu),
            ("Environment (.env)", _env_menu),
            ("Setup Wizards", _wizards_menu),
            ("API Keys", _show_api_keys),
            ("Return to Main Menu", None),
        ]
        for idx, (lbl, _) in enumerate(options, start=1):
            print(f"{idx}) {lbl}")
        choice = input("Select an option [1-5]: ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(options)):
            print_invalid_choice()
            continue
        idx = int(choice) - 1
        _, action = options[idx]
        if action is None:
            break
        action()
