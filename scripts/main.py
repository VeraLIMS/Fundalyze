# src/main.py

import sys
import os

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
from modules.generate_report import run_generate_report
from modules.management.note_manager import run_note_manager

SETTINGS = load_settings()


def exit_program():
    """Exit the entire application."""
    print("Exiting. Goodbye!")
    sys.exit(0)


def invalid_choice():
    """Handle invalid menu selection."""
    print("Invalid choice. Please select a valid option.\n")


def main():
    """
    Main menu loop. Each submenu is grouped into its own package:

      1) Manage Portfolio       → portfolio_manager/portfolio_manager.py
      2) Manage Groups          → group_analysis/group_analysis.py
      3) Generate Reports       → generate_report/run_generate_report()
      4) Exit
    """
    ACTIONS = [
        ("Manage Portfolio",               run_portfolio_manager),
        ("Manage Groups",                  run_group_analysis),
        ("Generate Reports (with metadata, fallback & Excel)", run_generate_report),
        ("Manage Notes",                  run_note_manager),
        ("Exit",                           exit_program),
    ]

    while True:
        print("\n=== Main Menu ===")
        for idx, (label, _) in enumerate(ACTIONS, start=1):
            print(f"  {idx}) {label}")
        choice = input(f"Enter 1-{len(ACTIONS)}: ").strip()

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(ACTIONS):
                _, action = ACTIONS[idx]
                action()
            else:
                invalid_choice()
        else:
            invalid_choice()


if __name__ == "__main__":
    main()
