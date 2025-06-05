#!/usr/bin/env python3
"""Command line entry point for the Fundalyze utilities.

This script exposes a simple CLI as well as an interactive menu which routes
to the various management tools bundled with Fundalyze.
"""

import sys
import os
import argparse
import textwrap
import subprocess

# Add the repository root to sys.path so 'modules' can be imported when this
# script is executed directly via `python scripts/main.py`.
SCRIPT_DIR = os.path.dirname(__file__)
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# Ensure environment variables from config/.env are loaded before other modules
from modules.config_utils import load_settings  # noqa: E402
from modules.interface import print_invalid_choice, print_header

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
    print_invalid_choice()


def run_portfolio_groups() -> None:
    """Combined menu for portfolio and group management."""
    from modules.management.portfolio_manager import portfolio_manager as pm
    from modules.management.group_analysis import group_analysis as ga

    portfolio = pm.load_portfolio(pm.PORTFOLIO_FILE)
    groups = ga.load_groups(ga.GROUPS_FILE)

    while True:
        print_header("🔁 Portfolio & Groups")
        print("--- Portfolio ---")
        print("1) View Portfolio")
        print("2) Add Ticker(s)")
        print("3) Update Ticker Data")
        print("4) Remove Ticker")
        print("--- Groups ---")
        print("5) View All Groups")
        print("6) Create New Group / Link Portfolio")
        print("7) Add Ticker(s) to Group")
        print("8) Remove Ticker from Group")
        print("9) Delete Group")
        print("10) Return to Main Menu")
        choice = input("Select an option [1-10]: ").strip()

        if choice == "1":
            pm.view_portfolio(portfolio)
        elif choice == "2":
            portfolio = pm.add_tickers(portfolio)
            pm.save_portfolio(portfolio, pm.PORTFOLIO_FILE)
        elif choice == "3":
            portfolio = pm.update_tickers(portfolio)
            pm.save_portfolio(portfolio, pm.PORTFOLIO_FILE)
        elif choice == "4":
            portfolio = pm.remove_ticker(portfolio)
            pm.save_portfolio(portfolio, pm.PORTFOLIO_FILE)
        elif choice == "5":
            ga.view_groups(groups)
        elif choice == "6":
            grp_name = ga.choose_group(portfolio)
            if not grp_name:
                print("No group name entered; canceling.\n")
            else:
                if grp_name in groups["Group"].values:
                    print(f"Group '{grp_name}' already exists.\n")
                else:
                    placeholder = {col: pm.pd.NA for col in ga.COLUMNS}
                    placeholder["Group"] = grp_name
                    placeholder["Ticker"] = ""
                    groups.loc[len(groups)] = placeholder
                    print(f"  ✓ Created new group '{grp_name}'.\n")
                ga.save_groups(groups, ga.GROUPS_FILE)
        elif choice == "7":
            if groups.empty:
                print("No groups exist. Create one first.\n")
            else:
                print("\nExisting groups:")
                unique_groups = groups["Group"].dropna().unique().tolist()
                for i, g in enumerate(unique_groups, start=1):
                    print(f"  {i}) {g}")
                sel = input(f"Select group (1-{len(unique_groups)}): ").strip()
                if sel.isdigit() and 1 <= int(sel) <= len(unique_groups):
                    grp_name = unique_groups[int(sel) - 1]
                    groups = ga.add_tickers_to_group(groups, grp_name)
                    ga.save_groups(groups, ga.GROUPS_FILE)
                else:
                    print_invalid_choice()
        elif choice == "8":
            groups = ga.remove_ticker_from_group(groups)
            ga.save_groups(groups, ga.GROUPS_FILE)
        elif choice == "9":
            groups = ga.delete_group(groups)
            ga.save_groups(groups, ga.GROUPS_FILE)
        elif choice == "10":
            break
        else:
            invalid_choice()


def _choose_tickers() -> list[str]:
    """Prompt for tickers using the report helper."""
    from modules.generate_report import _select_tickers

    return _select_tickers()


def run_reports_menu() -> None:
    """Sub-menu for report related utilities."""
    while True:
        print_header("\U0001F4D1 Reports")
        print("1) Full Workflow")
        print("2) Metadata Checker Only")
        print("3) Fallback Data Only")
        print("4) Excel Dashboard Only")
        print("5) Return to Main Menu")
        choice = input("Select an option [1-5]: ").strip()

        if choice == "1":
            run_generate_report()
        elif choice == "2":
            tickers = _choose_tickers()
            if tickers:
                run_metadata_checker(tickers)
        elif choice == "3":
            tickers = _choose_tickers()
            if tickers:
                run_fallback_data(tickers)
        elif choice == "4":
            tickers = _choose_tickers()
            if tickers:
                create_and_open_dashboard(tickers=tickers)
        elif choice == "5":
            break
        else:
            invalid_choice()


def run_tests_cli() -> None:
    """Run the test suite via the bundled helper script."""
    script = os.path.join(SCRIPT_DIR, "run_tests.py")
    subprocess.run([sys.executable, script])


def run_profile_cli() -> None:
    """Launch the performance profiling helper."""
    script = os.path.join(SCRIPT_DIR, "performance_profile.py")
    subprocess.run([sys.executable, script])


def run_utilities_menu() -> None:
    """Sub-menu exposing extra helper utilities."""
    while True:
        print_header("\U0001F6E0 Utilities")
        print("1) Run Test Suite")
        print("2) Performance Profile")
        print("3) Return to Main Menu")
        choice = input("Select an option [1-3]: ").strip()

        if choice == "1":
            run_tests_cli()
        elif choice == "2":
            run_profile_cli()
        elif choice == "3":
            break
        else:
            invalid_choice()


ACTION_ITEMS: list[tuple[str, callable]] = [
    ("Portfolio & Groups", run_portfolio_groups),
    ("Reports", run_reports_menu),
    ("Notes", run_note_manager),
    ("Directus Tools", run_directus_wizard),
    ("Settings", run_settings_manager),
    ("Utilities", run_utilities_menu),
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
    "tests": run_tests_cli,
    "profile": run_profile_cli,
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
    "tests": "Run unit tests",
    "profile": "Run performance profiler",
}


def interactive_menu():
    """
    Main menu loop displayed with simple numbered options.
    """
    actions = ACTION_ITEMS

    while True:
        print_header("📂 Main Menu")
        for idx, (label, _) in enumerate(actions, start=1):
            print(f"{idx}) {label}")
        choice = input(f"Select an option [1-{len(actions)}]: ").strip()

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
    examples = textwrap.dedent(
        """
        Examples:
          python scripts/main.py portfolio  # open portfolio manager
          python scripts/main.py report     # generate reports
          python scripts/main.py metadata   # run metadata checker
          python scripts/main.py tests      # execute test suite
        """
    )
    parser = argparse.ArgumentParser(
        description="Fundalyze command line interface",
        epilog=examples,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command")
    for cmd in COMMAND_MAP:
        sub.add_parser(
            cmd,
            help=COMMAND_HELP.get(cmd, cmd),
            description=COMMAND_HELP.get(cmd, cmd),
        )
    sub.add_parser("menu", help="Interactive menu (default)")
    parser.add_argument("--version", action="version", version="Fundalyze 1.0")
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
