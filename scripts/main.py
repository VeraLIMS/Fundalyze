#!/usr/bin/env python3
"""Command line entry point for the Fundalyze utilities.

This script exposes a simple CLI as well as an interactive menu which routes
to the various management tools bundled with Fundalyze.
"""

import sys
import os
import argparse

# Add the repository root to sys.path so 'modules' can be imported when this
# script is executed directly via `python scripts/main.py`.
SCRIPT_DIR = os.path.dirname(__file__)
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# Ensure environment variables from config/.env are loaded before other modules
from modules.config_utils import load_settings  # noqa: E402

from modules.management.portfolio_manager.portfolio_manager import main as run_portfolio_manager
from modules.management.group_analysis.group_analysis import main as run_group_analysis
from modules.generate_report import (
    run_generate_report,
    run_metadata_checker,
    run_fallback_data,
    create_and_open_dashboard,
)
from modules.management.note_manager import run_note_manager
from modules.management.settings_manager.settings_manager import (
    run_settings_manager,
)
from modules.management.directus_tools.directus_wizard import (
    run_directus_wizard,
)

SETTINGS = load_settings()


def exit_program():
    """Exit the entire application."""
    print("Exiting. Goodbye!")
    sys.exit(0)


def invalid_choice():
    """Handle invalid menu selection."""
    print("Invalid choice. Please select a valid option.\n")


ACTION_ITEMS: list[tuple[str, callable]] = [
    ("Manage Portfolio", run_portfolio_manager),
    ("Manage Groups", run_group_analysis),
    ("Generate Reports (with metadata, fallback & Excel)", run_generate_report),
    ("Manage Notes", run_note_manager),
    ("Manage Settings", run_settings_manager),
    ("Directus Wizard", run_directus_wizard),
    ("Exit", exit_program),
]

COMMAND_MAP: dict[str, callable] = {
    "portfolio": run_portfolio_manager,
    "groups": run_group_analysis,
    "report": run_generate_report,
    "notes": run_note_manager,
    "settings": run_settings_manager,
    "metadata": run_metadata_checker,
    "fallback": run_fallback_data,
    "dashboard": create_and_open_dashboard,
    "directus": run_directus_wizard,
}

COMMAND_HELP = {
    "portfolio": "Launch portfolio manager",
    "groups": "Launch group manager",
    "report": "Generate reports",
    "notes": "Launch note manager",
    "settings": "Edit configuration",
    "metadata": "Run metadata checker",
    "fallback": "Run fallback data fetch",
    "dashboard": "Create Excel dashboard",
    "directus": "Launch Directus wizard",
}


def interactive_menu():
    """
    Main menu loop. Each submenu is grouped into its own package:

      1) Manage Portfolio       → portfolio_manager/portfolio_manager.py
      2) Manage Groups          → group_analysis/group_analysis.py
      3) Generate Reports       → generate_report/run_generate_report()
      4) Manage Notes           → note_manager/run_note_manager()
      5) Manage Settings        → settings_manager/settings_manager.py
      6) Directus Wizard        → directus_tools/directus_wizard.py
      7) Exit
    """
    actions = ACTION_ITEMS

    while True:
        print("\n=== Main Menu ===")
        for idx, (label, _) in enumerate(actions, start=1):
            print(f"  {idx}) {label}")
        choice = input(f"Enter 1-{len(actions)}: ").strip()

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(actions):
                _, action = actions[idx]
                action()
            else:
                invalid_choice()
        else:
            invalid_choice()


def parse_args() -> argparse.Namespace:
    """Return parsed CLI arguments."""
    parser = argparse.ArgumentParser(description="Fundalyze command line interface")
    sub = parser.add_subparsers(dest="command")
    for cmd in COMMAND_MAP:
        sub.add_parser(cmd, help=COMMAND_HELP.get(cmd, cmd))
    sub.add_parser("menu", help="Interactive menu (default)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cmd = args.command or "menu"
    if cmd == "menu":
        interactive_menu()
        return

    action = COMMAND_MAP.get(cmd)
    if action:
        action()
    else:
        interactive_menu()


if __name__ == "__main__":
    main()
