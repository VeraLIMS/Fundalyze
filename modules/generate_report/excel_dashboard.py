# src/generate_report/excel_dashboard.py

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd

from modules.config_utils import get_output_dir
from modules.utils.data_utils import (
    ensure_period_column,
    read_csv_if_exists,
    strip_timezones,
)
from modules.utils.excel_utils import write_table
from modules.utils.progress_utils import progress_iter


def _load_ticker_data(td: Path) -> dict[str, pd.DataFrame]:
    """Return a mapping of CSV name → DataFrame for ``td``."""
    data: dict[str, pd.DataFrame] = {}

    df = read_csv_if_exists(td / "profile.csv")
    if df is not None:
        data["profile"] = strip_timezones(df)

    df = read_csv_if_exists(td / "1mo_prices.csv", parse_dates=["Date"])
    if df is not None:
        data["prices"] = strip_timezones(df)

    stmt_files = [
        "income_annual.csv",
        "income_quarter.csv",
        "balance_annual.csv",
        "balance_quarter.csv",
        "cash_annual.csv",
        "cash_quarter.csv",
    ]
    for fname in stmt_files:
        df = read_csv_if_exists(td / fname, index_col=0)
        if df is not None:
            df = ensure_period_column(df)
            data[fname.replace(".csv", "")] = strip_timezones(df)

    return data


def _assemble_tables(data_map: dict[str, dict[str, pd.DataFrame]]):
    """Return all dashboard DataFrames from raw ticker data."""
    profiles = {t: d.get("profile", pd.DataFrame()) for t, d in data_map.items()}
    prices = {t: d.get("prices", pd.DataFrame()) for t, d in data_map.items()}

    income_ann = {
        t: d.get("income_annual", pd.DataFrame()) for t, d in data_map.items()
    }
    income_qtr = {
        t: d.get("income_quarter", pd.DataFrame()) for t, d in data_map.items()
    }
    balance_ann = {
        t: d.get("balance_annual", pd.DataFrame()) for t, d in data_map.items()
    }
    balance_qtr = {
        t: d.get("balance_quarter", pd.DataFrame()) for t, d in data_map.items()
    }
    cash_ann = {t: d.get("cash_annual", pd.DataFrame()) for t, d in data_map.items()}
    cash_qtr = {t: d.get("cash_quarter", pd.DataFrame()) for t, d in data_map.items()}

    df_profiles = _safe_concat_normal(profiles)
    df_prices = _safe_concat_normal(prices)

    df_inc_ann = _transpose_financials(income_ann)
    df_inc_qtr = _transpose_financials(income_qtr)
    df_bal_ann = _transpose_financials(balance_ann)
    df_bal_qtr = _transpose_financials(balance_qtr)
    df_cash_ann = _transpose_financials(cash_ann)
    df_cash_qtr = _transpose_financials(cash_qtr)

    return (
        df_profiles,
        df_prices,
        df_inc_ann,
        df_inc_qtr,
        df_bal_ann,
        df_bal_qtr,
        df_cash_ann,
        df_cash_qtr,
    )


def _write_dashboard(
    dash_path: Path,
    df_profiles: pd.DataFrame,
    df_prices: pd.DataFrame,
    df_inc_ann: pd.DataFrame,
    df_inc_qtr: pd.DataFrame,
    df_bal_ann: pd.DataFrame,
    df_bal_qtr: pd.DataFrame,
    df_cash_ann: pd.DataFrame,
    df_cash_qtr: pd.DataFrame,
) -> None:
    """Write all tables to ``dash_path`` as an Excel workbook."""
    tables = [
        (df_profiles, "Profile", "Profile_Table", "Table Style Medium 2"),
        (df_prices, "PriceHistory", "PriceHistory_Table", "Table Style Medium 3"),
        (df_inc_ann, "Income_Annual", "Income_Annual_Table", "Table Style Medium 4"),
        (df_inc_qtr, "Income_Quarter", "Income_Quarter_Table", "Table Style Medium 5"),
        (df_bal_ann, "Balance_Annual", "Balance_Annual_Table", "Table Style Medium 6"),
        (df_bal_qtr, "Balance_Quarter", "Balance_Quarter_Table", "Table Style Medium 7"),
        (df_cash_ann, "Cash_Annual", "Cash_Annual_Table", "Table Style Medium 8"),
        (df_cash_qtr, "Cash_Quarter", "Cash_Quarter_Table", "Table Style Medium 9"),
    ]

    with pd.ExcelWriter(dash_path, engine="xlsxwriter") as writer:
        for df, sheet, table, style in tables:
            if not df.empty:
                write_table(writer, df, sheet, table, style=style)


def _strip_timezones(df: pd.DataFrame) -> pd.DataFrame:
    """Deprecated wrapper around :func:`modules.utils.data_utils.strip_timezones`."""
    return strip_timezones(df)


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

        # Ensure 'Period' exists for each statement DataFrame
        df = ensure_period_column(df)

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

    frames = [df.assign(Ticker=tk).loc[:, ["Ticker", *df.columns]] for tk, df in ticker_dfs.items()]
    return pd.concat(frames, axis=0, ignore_index=True, sort=True)




def create_dashboard(
    output_root: str | None = None,
    *,
    tickers: Optional[Iterable[str]] = None,
    progress: bool = False,
) -> Path:
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

    Parameters
    ----------
    output_root:
        Base folder containing ticker subdirectories.
    tickers:
        Optional subset of tickers to include. Defaults to all found in
        ``output_root``.
    progress:
        When ``True`` display a progress bar while loading CSV files.

    Returns:
        Path to the newly created .xlsx file.
    """
    if output_root is None:
        output_root = str(get_output_dir())

    root = Path(output_root)
    if not root.exists() or not root.is_dir():
        raise FileNotFoundError(f"Output folder '{output_root}' not found.")

    if tickers is None:
        ticker_dirs = sorted([p for p in root.iterdir() if p.is_dir()])
    else:
        ticker_dirs = [root / tk for tk in tickers if (root / tk).is_dir()]

    data_map: dict[str, dict[str, pd.DataFrame]] = {}
    iterator = ticker_dirs
    if progress:
        iterator = progress_iter(ticker_dirs, description="Loading")
    for td in iterator:
        data_map[td.name] = _load_ticker_data(td)

    (
        df_profiles,
        df_prices,
        df_inc_ann,
        df_inc_qtr,
        df_bal_ann,
        df_bal_qtr,
        df_cash_ann,
        df_cash_qtr,
    ) = _assemble_tables(data_map)

    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    dash_name = f"dashboard_{ts}.xlsx"
    dash_path = root / dash_name

    _write_dashboard(
        dash_path,
        df_profiles,
        df_prices,
        df_inc_ann,
        df_inc_qtr,
        df_bal_ann,
        df_bal_qtr,
        df_cash_ann,
        df_cash_qtr,
    )

    return dash_path


def show_dashboard_in_excel(dashboard_path: Path):
    """
    Open the newly created Excel file in the OS default application.
    """
    if not dashboard_path.exists():
        raise FileNotFoundError(f"Dashboard file not found: {dashboard_path}")

    if sys.platform.startswith("win") and hasattr(os, "startfile"):
        getattr(os, "startfile")(str(dashboard_path))  # pylint: disable=no-member
    elif sys.platform.startswith("darwin"):
        subprocess.call(["open", str(dashboard_path)])
    else:
        subprocess.call(["xdg-open", str(dashboard_path)])


def create_and_open_dashboard(
    output_root: str | None = None,
    *,
    tickers: Optional[Iterable[str]] = None,
    progress: bool = False,
):
    """
    Create an Excel dashboard (with named Tables) and open it automatically.

    Parameters
    ----------
    output_root:
        Base folder containing ticker subdirectories.
    tickers:
        Optional subset of tickers to include.
    progress:
        When ``True`` display a progress bar while loading CSV files.
    """
    dash_path = create_dashboard(
        output_root=output_root, tickers=tickers, progress=progress
    )
    print(f"\n✅ Excel dashboard created at:\n   {dash_path}\n")
    print("Opening it now…\n")
    show_dashboard_in_excel(dash_path)
