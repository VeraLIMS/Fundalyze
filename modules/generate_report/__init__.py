# src/generate_report/__init__.py

from .report_generator import fetch_and_compile
from .metadata_checker import main as run_metadata_checker, run_for_tickers
from .fallback_data import run_fallback_data
from .excel_dashboard import create_and_open_dashboard

from modules.management.portfolio_manager.portfolio_manager import (
    load_portfolio,
    PORTFOLIO_FILE,
)
from modules.management.group_analysis.group_analysis import (
    load_groups,
    GROUPS_FILE,
)


def _select_tickers() -> list[str]:
    """Prompt user to choose tickers manually, from portfolio or from a group."""
    print("\nChoose ticker source:")
    print("  1) Enter ticker symbols manually")
    print("  2) Use all tickers from portfolio")
    print("  3) Choose a group")
    choice = input("Select 1/2/3: ").strip()

    if choice == "1":
        raw = input("Enter ticker symbol(s), comma-separated): ").strip()
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
        sel = input(f"Select group 1-{len(names)}: ").strip()
        if sel.isdigit() and 1 <= int(sel) <= len(names):
            grp = names[int(sel) - 1]
            df = groups[groups["Group"] == grp]
            return df["Ticker"].dropna().astype(str).str.upper().unique().tolist()
        print("Invalid selection.\n")
        return []

    print("Invalid choice.\n")
    return []


def run_generate_report():
    """
    1) Ask user for tickers.
    2) fetch_and_compile(...) for each.
    3) run metadata checker.
    4) run fallback data.
    5) build and open an Excel dashboard.
    """
    print("\n=== Generate Reports (with metadata check + fallback) ===")
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
        create_and_open_dashboard(output_root="output", tickers=tickers)
    except Exception as e:
        print(f"[ERROR] Could not create/open Excel dashboard: {e}")

    print("\n[Done] Returning to main menu.\n")
