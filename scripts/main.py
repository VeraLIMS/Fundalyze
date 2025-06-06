#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# Fundalyze CLI main entry point.
# Provides an interactive menu as well as direct command execution for
# portfolio management and other helpers.
# ---------------------------------------------------------------------------
"""Command line entry point for the Fundalyze utilities.

This script exposes a simple CLI as well as an interactive menu which routes
to the various management tools bundled with Fundalyze.

Menu map::

    1. Portfolio & Groups  -> portfolio and group management
    2. Notes               -> note manager
    3. Directus Tools      -> Directus wizard utilities
    4. Settings            -> edit configuration
    5. Utilities           -> run tests & profiler
    6. Exit                -> quit the application

Flow chart::

    interactive_menu()
        ├─ run_portfolio_groups()
        ├─ run_note_manager()
        ├─ run_directus_wizard()
        ├─ run_settings_manager()
        ├─ run_utilities_menu()
        └─ exit_program()

You can also call this script with a subcommand such as ``portfolio`` to skip
the menu entirely.
"""

import sys
import os
import argparse
import textwrap
import subprocess
import json
from pathlib import Path
from typing import Callable

# Add the repository root to sys.path so 'modules' can be imported when this
# script is executed directly via `python scripts/main.py`.
SCRIPT_DIR = os.path.dirname(__file__)
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from modules.logging_utils import setup_logging

setup_logging("logs/fundalyze.log")

# Ensure environment variables from config/.env are loaded before other modules
from modules.config_utils import load_settings  # noqa: E402
from modules.interface import (
    print_invalid_choice,
    print_header,
    print_menu,
    print_table,
)

from modules.management.portfolio_manager.portfolio_manager import (
    main as run_portfolio_manager,
)
from modules.management.group_analysis.group_analysis import main as run_group_analysis
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

    portfolio = pm.load_portfolio()
    groups = ga.load_groups()

    while True:
        print_header("🔁 Portfolio & Groups")
        options = [
            "View Portfolio",
            "Add Ticker(s)",
            "Update Ticker Data",
            "Remove Ticker",
            "View All Groups",
            "Create New Group / Link Portfolio",
            "Add Ticker(s) to Group",
            "Remove Ticker from Group",
            "Delete Group",
            "Return to Main Menu",
        ]
        print_menu(options)
        choice = input(f"Select an option [1-{len(options)}]: ").strip()

        if choice == "1":
            pm.view_portfolio(portfolio)
        elif choice == "2":
            portfolio = pm.add_tickers(portfolio)
            pm.save_portfolio(portfolio)
        elif choice == "3":
            portfolio = pm.update_tickers(portfolio)
            pm.save_portfolio(portfolio)
        elif choice == "4":
            portfolio = pm.remove_ticker(portfolio)
            pm.save_portfolio(portfolio)
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
                ga.save_groups(groups)
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
                    ga.save_groups(groups)
                else:
                    print_invalid_choice()
        elif choice == "8":
            groups = ga.remove_ticker_from_group(groups)
            ga.save_groups(groups)
        elif choice == "9":
            groups = ga.delete_group(groups)
            ga.save_groups(groups)
        elif choice == "10":
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


def view_directus_portfolio() -> None:
    """Display portfolio items stored in Directus."""
    from modules.management.portfolio_manager.portfolio_manager import load_portfolio

    df = load_portfolio()
    if df.empty:
        print("Portfolio is empty.\n")
    else:
        print_table(df)


def view_directus_profiles() -> None:
    """Display company profiles stored in Directus."""
    from modules.data.directus_client import fetch_items
    import pandas as pd

    records = fetch_items("company_profiles")
    if not records:
        print("No profiles found.\n")
        return
    df = pd.DataFrame(records)
    print_table(df)


def debug_mapped_record() -> None:
    """Fetch and display a single mapped portfolio record without inserting."""
    from modules.management.portfolio_manager.portfolio_manager import (
        fetch_from_unified,
        get_portfolio_collection,
    )
    from modules.data.directus_mapper import prepare_records

    ticker = input("Ticker to map: ").strip().upper()
    if not ticker:
        print("No ticker provided.\n")
        return
    try:
        record = fetch_from_unified(ticker)
    except Exception as exc:  # pragma: no cover - user input/network
        print(f"Error fetching data: {exc}\n")
        return

    print("Original record:\n", record)
    try:
        collection = get_portfolio_collection()
        mapped = prepare_records(collection, [record])[0]
    except Exception as exc:
        print(f"Mapping failed: {exc}\n")
        return

    print("Mapped record:\n", mapped)


def run_mapping_test() -> None:
    """Display current field mapping for portfolio and groups."""
    subprocess.run([sys.executable, os.path.join(SCRIPT_DIR, "mapping_diagnostic.py")])


def run_insert_test() -> None:
    """Insert a test record for ticker MSFT and show the result."""
    subprocess.run([
        sys.executable,
        os.path.join(SCRIPT_DIR, "mapping_diagnostic.py"),
        "--insert",
    ])


def run_add_missing_cli() -> None:
    """Update field map using a JSON file of records."""
    collection = input("Collection name: ").strip()
    if not collection:
        print("No collection provided.\n")
        return
    path = input("Path to JSON file: ").strip()
    if not path:
        print("No file provided.\n")
        return
    try:
        data = json.loads(Path(path).read_text())
    except Exception as exc:  # pragma: no cover - user input
        print(f"Error reading file: {exc}\n")
        return
    if isinstance(data, dict):
        records = [data]
    elif isinstance(data, list):
        records = data
    else:
        print("JSON must be an object or list of objects.\n")
        return
    from modules.data.directus_mapper import add_missing_mappings

    add_missing_mappings(collection, records)
    print("Mapping updated.\n")


def run_mapping_validator_cli() -> None:
    """Validate field mapping against a JSON file and optionally insert."""
    collection = input("Collection name: ").strip()
    if not collection:
        print("No collection provided.\n")
        return
    path = input("Path to JSON file: ").strip()
    if not path:
        print("No file provided.\n")
        return
    cmd = [sys.executable, os.path.join(SCRIPT_DIR, "mapping_validator.py"), collection, path]
    resp = input("Insert into Directus after validation? (y/N): ").strip().lower()
    if resp in ("y", "yes"):
        cmd.append("--insert")
    subprocess.run(cmd)


def portfolio_summary_cli() -> None:
    """Display portfolio summary statistics and missing-field counts."""
    from modules.management.portfolio_manager.portfolio_manager import load_portfolio
    from modules.analytics import portfolio_summary, sector_counts, missing_field_counts

    df = load_portfolio()
    if df.empty:
        print("Portfolio is empty.\n")
        return

    print_header("\U0001F4CA Portfolio Summary")
    summary = portfolio_summary(df)
    if not summary.empty:
        print_table(summary, showindex=True)

    counts = sector_counts(df)
    if not counts.empty:
        print("\nSectors:")
        print_table(counts)

    missing = missing_field_counts(df)
    if not missing.empty:
        print("\nMissing Fields:")
        print_table(missing)


def schema_export_cli() -> None:
    """Export Directus schema definitions to a CSV file."""
    from modules.schema import export_schema
    from modules.api import DirectusClient

    path = input(
        "Output CSV path [config/schema_definitions_export.csv]: ").strip()
    if not path:
        path = "config/schema_definitions_export.csv"
    export_schema(DirectusClient(), path)


def schema_sync_cli() -> None:
    """Synchronize CSV schema definitions with Directus."""
    from modules.schema import sync_schema
    from modules.api import DirectusClient

    csv_path = input(
        "Schema CSV path [config/schema_definitions.csv]: ").strip()
    if not csv_path:
        csv_path = "config/schema_definitions.csv"
    resp = input("Delete fields not in CSV? (y/N): ").strip().lower()
    remove = resp in ("y", "yes")
    sync_schema(csv_path, DirectusClient(), remove_extra=remove)


def run_schema_menu() -> None:
    """Interactive menu for Directus schema utilities."""
    while True:
        print_header("\U0001F4C1 Schema Tools")
        options = ["Export Schema", "Sync Schema", "Return to Main Menu"]
        print_menu(options)
        choice = input(f"Select an option [1-{len(options)}]: ").strip()

        if choice == "1":
            schema_export_cli()
        elif choice == "2":
            schema_sync_cli()
        elif choice == "3":
            break
        else:
            invalid_choice()


def run_utilities_menu() -> None:
    """Sub-menu exposing extra helper utilities."""
    while True:
        print_header("\U0001f6e0 Utilities")
        options = [
            "Run Test Suite",
            "Performance Profile",
            "Test Mapping",
            "Test Insert",
            "Validate Mapping",
            "Return to Main Menu",
        ]
        print_menu(options)
        choice = input(f"Select an option [1-{len(options)}]: ").strip()

        if choice == "1":
            run_tests_cli()
        elif choice == "2":
            run_profile_cli()
        elif choice == "3":
            run_mapping_test()
        elif choice == "4":
            run_insert_test()
        elif choice == "5":
            run_mapping_validator_cli()
        elif choice == "6":
            break
        else:
            invalid_choice()


ACTION_ITEMS: list[tuple[str, Callable[[], None]]] = [
    ("Portfolio & Groups", run_portfolio_groups),
    ("Notes", run_note_manager),
    ("Directus Tools", run_directus_wizard),
    ("Settings", run_settings_manager),
    ("Schema Tools", run_schema_menu),
    ("Utilities", run_utilities_menu),
    ("Exit", exit_program),
]

COMMAND_MAP: dict[str, Callable[[], None]] = {
    "portfolio": run_portfolio_manager,
    "groups": run_group_analysis,
    "notes": run_note_manager,
    "settings": run_settings_manager,
    "directus": run_directus_wizard,
    "schema-menu": run_schema_menu,
    "schema-export": schema_export_cli,
    "schema-sync": schema_sync_cli,
    "tests": run_tests_cli,
    "profile": run_profile_cli,
    "view-portfolio": view_directus_portfolio,
    "view-profiles": view_directus_profiles,
    "map-record": debug_mapped_record,
    "diag": lambda: subprocess.run(["python", "scripts/mapping_diagnostic.py"]),
    "test-mapping": run_mapping_test,
    "test-insert": run_insert_test,
    "add-missing": run_add_missing_cli,
    "validate-mapping": run_mapping_validator_cli,
    "summary": portfolio_summary_cli,
}

COMMAND_HELP = {
    "portfolio": "Launch portfolio manager",
    "groups": "Launch group manager",
    "notes": "Launch note manager",
    "settings": "Edit configuration",
    "directus": "Launch Directus wizard",
    "schema-menu": "Interactive schema utilities",
    "schema-export": "Export Directus schema to CSV",
    "schema-sync": "Sync CSV schema to Directus",
    "tests": "Run unit tests",
    "profile": "Run performance profiler",
    "view-portfolio": "View portfolio from Directus",
    "view-profiles": "View company profiles from Directus",
    "map-record": "Fetch and display mapped portfolio record",
    "diag": "Run mapping diagnostic script",
    "test-mapping": "Display current field mapping",
    "test-insert": "Insert a test record into Directus",
    "add-missing": "Add unmapped fields to directus_field_map.json",
    "validate-mapping": "Validate and optionally insert a JSON dataset",
    "summary": "Display portfolio summary statistics",
}


def interactive_menu():
    """
    Main menu loop displayed with simple numbered options.
    """
    actions = ACTION_ITEMS

    while True:
        print_header("📂 Main Menu")
        print_menu([label for label, _ in actions])
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
          python scripts/main.py summary    # show portfolio statistics
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
    parser.add_argument(
        "--no-openbb",
        action="store_true",
        help="Disable OpenBB when fetching company data",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.no_openbb:
        from modules.data import unified_fetcher

        unified_fetcher.DEFAULT_USE_OPENBB = False
    cmd = args.command or "menu"
    if cmd == "menu":
        interactive_menu()
        return

    action = COMMAND_MAP.get(cmd)
    if action:
        action()
    else:
        print(f"Unknown command: {cmd}\n")
        interactive_menu()


if __name__ == "__main__":
    main()
