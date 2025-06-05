"""Small text-based UI helpers used by the command line tools."""

from __future__ import annotations

import pandas as pd
from tabulate import tabulate

INVALID_CHOICE_MSG = (
    "Invalid choice. Enter a number from the menu or press Ctrl+C to exit. "
    "Run 'python scripts/main.py --help' for usage.\n"
)


def print_header(title: str) -> None:
    """Display a section heading consistently across menus."""
    print(f"\n=== {title} ===")


def print_table(df: pd.DataFrame, *, showindex: bool = False) -> None:
    """Pretty-print a DataFrame using :mod:`tabulate`."""
    if df is None or df.empty:
        print("(no data)")
        return
    print(tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=showindex))


def print_invalid_choice() -> None:
    """Standard message for invalid menu selections."""
    print(INVALID_CHOICE_MSG)


def input_or_cancel(prompt: str) -> str:
    """Return user input or an empty string if canceled."""
    return input(f"{prompt} (or press Enter to cancel): ").strip()


def print_menu(options: list[str]) -> None:
    """Display a numbered menu list."""
    for idx, label in enumerate(options, start=1):
        print(f"{idx}) {label}")
