# src/generate_report/excel_dashboard.py

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

import pandas as pd


def _col_to_letter(idx: int) -> str:
    """Return Excel-style column letters (0-based)."""
    letters = ""
    while idx >= 0:
        idx, rem = divmod(idx, 26)
        letters = chr(65 + rem) + letters
        idx -= 1
    return letters


def _transpose_financials(ticker_dfs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Given ticker_dfs mapping ticker → DataFrame (with a 'Period' column plus metrics),
    produce one wide DataFrame where:
      - Column A: 'Ticker'
      - Column B: 'Metric'
      - Columns C…: each distinct Period (as string)
    Rows stack one ticker-block after another.

    We convert any non-string column names (e.g. Timestamp) into strings,
    so that Excel table headers are valid.
    """
    all_blocks = []

    for ticker, df in ticker_dfs.items():
        if df.empty:
            continue

        # Ensure 'Period' is a column
        if "Period" not in df.columns:
            df = df.reset_index().rename(columns={"index": "Period"})

        temp = df.copy().set_index("Period")
        # Now temp.index = periods, temp.columns = metrics
        transposed = temp.T

        # Convert period column names (index of temp) to strings
        # Using vectorized conversion avoids the Python-level loop
        transposed.columns = [str(col) for col in transposed.columns]

        # Insert 'Ticker' in column A
        transposed.insert(0, "Ticker", ticker)
        # Insert 'Metric' in column B (old index)
        transposed.insert(1, "Metric", transposed.index)

        transposed = transposed.reset_index(drop=True)
        all_blocks.append(transposed)

    if not all_blocks:
        return pd.DataFrame()

    return pd.concat(all_blocks, axis=0, ignore_index=True, sort=False)


def _safe_concat_normal(ticker_dfs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    For non‐financial sheets (Profile, PriceHistory), simply stack each DataFrame
    with an added 'Ticker' column at the front.
    """
    if not ticker_dfs:
        return pd.DataFrame()

    frames = []
    for tk, df in ticker_dfs.items():
        df_copy = df.copy()
        df_copy.insert(0, "Ticker", tk)
        frames.append(df_copy)

    return pd.concat(frames, axis=0, ignore_index=True, sort=True)


def create_dashboard(output_root: str = "output") -> Path:
    """
    1) Find subfolders under output_root (one per ticker).
    2) Read these CSVs if present:
         - profile.csv
         - 1mo_prices.csv
         - income_annual.csv
         - income_quarter.csv
         - balance_annual.csv
         - balance_quarter.csv
         - cash_annual.csv
         - cash_quarter.csv

    3) Build two “normal” DataFrames:
         df_profiles = _safe_concat_normal(profiles)
         df_prices   = _safe_concat_normal(prices)

       And six “transposed” DataFrames (with stringified period headers):
         df_inc_ann  = _transpose_financials(income_ann)
         df_inc_qtr  = _transpose_financials(income_qtr)
         df_bal_ann  = _transpose_financials(balance_ann)
         df_bal_qtr  = _transpose_financials(balance_qtr)
         df_cash_ann = _transpose_financials(cash_ann)
         df_cash_qtr = _transpose_financials(cash_qtr)

    4) Write all eight DataFrames to:
         output_root/dashboard_<TIMESTAMP>.xlsx
       Converting each sheet into an Excel Table (so you can use structured references
       like `[Revenue]` or `[2022-12]` in formulas).

    Returns:
        Path to the newly created .xlsx file.
    """
    root = Path(output_root)
    if not root.exists() or not root.is_dir():
        raise FileNotFoundError(f"Output folder '{output_root}' not found.")

    ticker_dirs = sorted([p for p in root.iterdir() if p.is_dir()])

    profiles = {}
    prices = {}
    income_ann = {}
    income_qtr = {}
    balance_ann = {}
    balance_qtr = {}
    cash_ann = {}
    cash_qtr = {}

    for td in ticker_dirs:
        ticker = td.name

        # ── Profile ─────────────────────────────────────────────────
        profile_path = td / "profile.csv"
        if profile_path.exists():
            try:
                df = pd.read_csv(profile_path)
                profiles[ticker] = df
            except Exception:
                pass

        # ── 1mo_prices ───────────────────────────────────────────────
        price_path = td / "1mo_prices.csv"
        if price_path.exists():
            try:
                df = pd.read_csv(price_path, parse_dates=["Date"])
                prices[ticker] = df
            except Exception:
                pass

        # ── Income Annual ───────────────────────────────────────────
        ia_path = td / "income_annual.csv"
        if ia_path.exists():
            try:
                df = pd.read_csv(ia_path, index_col=0, parse_dates=True)
                df = df.reset_index().rename(columns={"index": "Period"})
                income_ann[ticker] = df
            except Exception:
                pass

        # ── Income Quarterly ────────────────────────────────────────
        iq_path = td / "income_quarter.csv"
        if iq_path.exists():
            try:
                df = pd.read_csv(iq_path, index_col=0, parse_dates=True)
                df = df.reset_index().rename(columns={"index": "Period"})
                income_qtr[ticker] = df
            except Exception:
                pass

        # ── Balance Annual ──────────────────────────────────────────
        ba_path = td / "balance_annual.csv"
        if ba_path.exists():
            try:
                df = pd.read_csv(ba_path, index_col=0, parse_dates=True)
                df = df.reset_index().rename(columns={"index": "Period"})
                balance_ann[ticker] = df
            except Exception:
                pass

        # ── Balance Quarterly ───────────────────────────────────────
        bq_path = td / "balance_quarter.csv"
        if bq_path.exists():
            try:
                df = pd.read_csv(bq_path, index_col=0, parse_dates=True)
                df = df.reset_index().rename(columns={"index": "Period"})
                balance_qtr[ticker] = df
            except Exception:
                pass

        # ── Cash Annual ─────────────────────────────────────────────
        ca_path = td / "cash_annual.csv"
        if ca_path.exists():
            try:
                df = pd.read_csv(ca_path, index_col=0, parse_dates=True)
                df = df.reset_index().rename(columns={"index": "Period"})
                cash_ann[ticker] = df
            except Exception:
                pass

        # ── Cash Quarterly ──────────────────────────────────────────
        cq_path = td / "cash_quarter.csv"
        if cq_path.exists():
            try:
                df = pd.read_csv(cq_path, index_col=0, parse_dates=True)
                df = df.reset_index().rename(columns={"index": "Period"})
                cash_qtr[ticker] = df
            except Exception:
                pass

    # Build “normal” tables
    df_profiles = _safe_concat_normal(profiles)
    df_prices   = _safe_concat_normal(prices)

    # Build “transposed” tables (stringify Period headers)
    df_inc_ann  = _transpose_financials(income_ann)
    df_inc_qtr  = _transpose_financials(income_qtr)
    df_bal_ann  = _transpose_financials(balance_ann)
    df_bal_qtr  = _transpose_financials(balance_qtr)
    df_cash_ann = _transpose_financials(cash_ann)
    df_cash_qtr = _transpose_financials(cash_qtr)

    # Create timestamped filename
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    dash_name = f"dashboard_{ts}.xlsx"
    dash_path = root / dash_name

    # Write to Excel, adding each sheet as a named Table
    with pd.ExcelWriter(dash_path, engine="xlsxwriter") as writer:

        # ── Sheet: Profile ───────────────────────────────────────────
        if not df_profiles.empty:
            sheet_name = "Profile"
            df_profiles.to_excel(writer, sheet_name=sheet_name, index=False)
            worksheet = writer.sheets[sheet_name]

            nrows, ncols = df_profiles.shape
            last_row = nrows      # header is row 0, data runs 1..nrows
            last_col = ncols - 1
            # e.g. "A1:E101" if 100 data rows and 5 columns total
            table_range = f"A1:{_col_to_letter(last_col)}{last_row + 1}"
            worksheet.add_table(
                table_range,
                {
                    "name":       "Profile_Table",
                    "columns":    [{"header": col} for col in df_profiles.columns],
                    "autofilter": True,
                    "style":      "Table Style Medium 2",
                },
            )

        # ── Sheet: PriceHistory ───────────────────────────────────────
        if not df_prices.empty:
            sheet_name = "PriceHistory"
            df_prices.to_excel(writer, sheet_name=sheet_name, index=False)
            worksheet = writer.sheets[sheet_name]

            nrows, ncols = df_prices.shape
            last_row = nrows
            last_col = ncols - 1
            table_range = f"A1:{_col_to_letter(last_col)}{last_row + 1}"
            worksheet.add_table(
                table_range,
                {
                    "name":       "PriceHistory_Table",
                    "columns":    [{"header": col} for col in df_prices.columns],
                    "autofilter": True,
                    "style":      "Table Style Medium 3",
                },
            )

        # ── Sheet: Income_Annual ───────────────────────────────────────
        if not df_inc_ann.empty:
            sheet_name = "Income_Annual"
            df_inc_ann.to_excel(writer, sheet_name=sheet_name, index=False)
            worksheet = writer.sheets[sheet_name]

            nrows, ncols = df_inc_ann.shape
            last_row = nrows
            last_col = ncols - 1
            table_range = f"A1:{_col_to_letter(last_col)}{last_row + 1}"
            worksheet.add_table(
                table_range,
                {
                    "name":       "Income_Annual_Table",
                    "columns":    [{"header": col} for col in df_inc_ann.columns],
                    "autofilter": True,
                    "style":      "Table Style Medium 4",
                },
            )

        # ── Sheet: Income_Quarter ─────────────────────────────────────
        if not df_inc_qtr.empty:
            sheet_name = "Income_Quarter"
            df_inc_qtr.to_excel(writer, sheet_name=sheet_name, index=False)
            worksheet = writer.sheets[sheet_name]

            nrows, ncols = df_inc_qtr.shape
            last_row = nrows
            last_col = ncols - 1
            table_range = f"A1:{_col_to_letter(last_col)}{last_row + 1}"
            worksheet.add_table(
                table_range,
                {
                    "name":       "Income_Quarter_Table",
                    "columns":    [{"header": col} for col in df_inc_qtr.columns],
                    "autofilter": True,
                    "style":      "Table Style Medium 5",
                },
            )

        # ── Sheet: Balance_Annual ─────────────────────────────────────
        if not df_bal_ann.empty:
            sheet_name = "Balance_Annual"
            df_bal_ann.to_excel(writer, sheet_name=sheet_name, index=False)
            worksheet = writer.sheets[sheet_name]

            nrows, ncols = df_bal_ann.shape
            last_row = nrows
            last_col = ncols - 1
            table_range = f"A1:{_col_to_letter(last_col)}{last_row + 1}"
            worksheet.add_table(
                table_range,
                {
                    "name":       "Balance_Annual_Table",
                    "columns":    [{"header": col} for col in df_bal_ann.columns],
                    "autofilter": True,
                    "style":      "Table Style Medium 6",
                },
            )

        # ── Sheet: Balance_Quarter ────────────────────────────────────
        if not df_bal_qtr.empty:
            sheet_name = "Balance_Quarter"
            df_bal_qtr.to_excel(writer, sheet_name=sheet_name, index=False)
            worksheet = writer.sheets[sheet_name]

            nrows, ncols = df_bal_qtr.shape
            last_row = nrows
            last_col = ncols - 1
            table_range = f"A1:{_col_to_letter(last_col)}{last_row + 1}"
            worksheet.add_table(
                table_range,
                {
                    "name":       "Balance_Quarter_Table",
                    "columns":    [{"header": col} for col in df_bal_qtr.columns],
                    "autofilter": True,
                    "style":      "Table Style Medium 7",
                },
            )

        # ── Sheet: Cash_Annual ────────────────────────────────────────
        if not df_cash_ann.empty:
            sheet_name = "Cash_Annual"
            df_cash_ann.to_excel(writer, sheet_name=sheet_name, index=False)
            worksheet = writer.sheets[sheet_name]

            nrows, ncols = df_cash_ann.shape
            last_row = nrows
            last_col = ncols - 1
            table_range = f"A1:{_col_to_letter(last_col)}{last_row + 1}"
            worksheet.add_table(
                table_range,
                {
                    "name":       "Cash_Annual_Table",
                    "columns":    [{"header": col} for col in df_cash_ann.columns],
                    "autofilter": True,
                    "style":      "Table Style Medium 8",
                },
            )

        # ── Sheet: Cash_Quarter ───────────────────────────────────────
        if not df_cash_qtr.empty:
            sheet_name = "Cash_Quarter"
            df_cash_qtr.to_excel(writer, sheet_name=sheet_name, index=False)
            worksheet = writer.sheets[sheet_name]

            nrows, ncols = df_cash_qtr.shape
            last_row = nrows
            last_col = ncols - 1
            table_range = f"A1:{_col_to_letter(last_col)}{last_row + 1}"
            worksheet.add_table(
                table_range,
                {
                    "name":       "Cash_Quarter_Table",
                    "columns":    [{"header": col} for col in df_cash_qtr.columns],
                    "autofilter": True,
                    "style":      "Table Style Medium 9",
                },
            )

    return dash_path


def show_dashboard_in_excel(dashboard_path: Path):
    """
    Open the newly created Excel file in the OS default application.
    """
    if not dashboard_path.exists():
        raise FileNotFoundError(f"Dashboard file not found: {dashboard_path}")

    if sys.platform.startswith("win"):
        os.startfile(str(dashboard_path))
    elif sys.platform.startswith("darwin"):
        subprocess.call(["open", str(dashboard_path)])
    else:
        subprocess.call(["xdg-open", str(dashboard_path)])


def create_and_open_dashboard(output_root: str = "output"):
    """
    Create an Excel dashboard (with named Tables) and open it automatically.
    """
    dash_path = create_dashboard(output_root=output_root)
    print(f"\n✅ Excel dashboard created at:\n   {dash_path}\n")
    print("Opening it now…\n")
    show_dashboard_in_excel(dash_path)
