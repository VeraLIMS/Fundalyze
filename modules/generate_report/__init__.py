"""Convenience wrappers for generating ticker reports and dashboards."""

# src/generate_report/__init__.py
"""Convenience entry points for the report-generation workflow.

The :mod:`generate_report` package orchestrates fetching data, fixing missing
files and building an Excel dashboard.  ``fetch_and_compile`` collects the raw
datasets and Markdown report, ``run_for_tickers`` repairs failed downloads,
``run_fallback_data`` performs a last-resort yfinance pull, and
``create_and_open_dashboard`` produces the final Excel workbook.
"""

from .report_generator import fetch_and_compile
from .metadata_checker import run_for_tickers
from .fallback_data import run_fallback_data
from .excel_dashboard import create_and_open_dashboard

# Backwards compatible alias used by `scripts/main.py`
run_metadata_checker = run_for_tickers

from modules.management.portfolio_manager.portfolio_manager import (
    load_portfolio,
    PORTFOLIO_FILE,
)
from modules.management.group_analysis.group_analysis import (
    load_groups,
    GROUPS_FILE,
)
from modules.interface import print_invalid_choice, print_header, print_menu


def _select_tickers() -> list[str]:
    """Prompt user to choose tickers manually, from portfolio or a group."""
    print_header("📑 Reports")
    options = [
        "Enter ticker symbols manually",
        "Use all tickers from portfolio",
        "Choose a group",
        "Return to Main Menu",
    ]
    print_menu(options)
    choice = input(f"Select an option [1-{len(options)}]: ").strip()

    if choice == "1":
        raw = input(
            "Enter ticker symbol(s), comma-separated (or press Enter to cancel): "
        ).strip()
        if not raw:
            print("No tickers entered.\n")
            return []
        return [t.strip().upper() for t in raw.split(",") if t.strip()]

    if choice == "2":
        pf = load_portfolio(PORTFOLIO_FILE)
        return pf["Ticker"].dropna().astype(str).str.upper().unique().tolist()

    if choice == "3":
        groups = load_groups(GROUPS_FILE)
        names = groups["Group"].dropna().unique().tolist()
        if not names:
            print("No groups defined.\n")
            return []
        for i, g in enumerate(names, start=1):
            print(f"  {i}) {g}")
        sel = input(
            f"Select a group [1-{len(names)}] (or press Enter to cancel): "
        ).strip()
        if not sel:
            print("Canceled.\n")
            return []
        if sel.isdigit() and 1 <= int(sel) <= len(names):
            grp = names[int(sel) - 1]
            df = groups[groups["Group"] == grp]
            return df["Ticker"].dropna().astype(str).str.upper().unique().tolist()
        print_invalid_choice()
        return []

    if choice == "4":
        return []
    print_invalid_choice()
    return []


def run_generate_report():
    """
    1) Ask user for tickers.
    2) fetch_and_compile(...) for each.
    3) run metadata checker.
    4) run fallback data.
    5) build and open an Excel dashboard.
    """
    print_header("📑 Reports")
    print("Generate reports (metadata, fallback & Excel export).")
    tickers = _select_tickers()
    if not tickers:
        print("No tickers selected. Returning to main menu.\n")
        return
    for tk in tickers:
        try:
            fetch_and_compile(tk)
        except Exception as e:
            print(f"  ⚠ Error while generating report for {tk}: {e}")

    print("\n--- Running metadata checker on output/ ---")
    run_for_tickers(tickers)

    print("\n--- Attempting to re-fetch missing data (fallback) ---")
    run_fallback_data(tickers)

    # ─────────────────────────────────────────────────────────────────
    # Now create and open the Excel dashboard. Any exception will be printed.
    try:
        create_and_open_dashboard(tickers=tickers)
    except Exception as e:
        print(f"[ERROR] Could not create/open Excel dashboard: {e}")

    print("\n[Done] Returning to main menu.\n")
