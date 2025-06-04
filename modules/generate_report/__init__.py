# src/generate_report/__init__.py

from .report_generator import fetch_and_compile
from .metadata_checker import main as run_metadata_checker, run_for_tickers
from .fallback_data import run_fallback_data
from .excel_dashboard import create_and_open_dashboard


def run_generate_report():
    """
    1) Ask user for tickers.
    2) fetch_and_compile(...) for each.
    3) run metadata checker.
    4) run fallback data.
    5) build and open an Excel dashboard.
    """
    print("\n=== Generate Reports (with metadata check + fallback) ===")
    raw = input("Enter ticker symbol(s), comma-separated): ").strip()
    if not raw:
        print("No tickers entered. Returning to main menu.\n")
        return

    tickers = [t.strip().upper() for t in raw.split(",") if t.strip()]
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
        create_and_open_dashboard(output_root="output")
    except Exception as e:
        print(f"[ERROR] Could not create/open Excel dashboard: {e}")

    print("\n[Done] Returning to main menu.\n")
