#!/usr/bin/env python3
# metadata_checker.py

"""Validate downloaded datasets and attempt targeted repairs.

``metadata_checker.py`` scans each ``metadata.json`` under ``output/<TICKER>/``
for entries whose ``source`` value begins with ``ERROR``.  Those files are
re‑fetched using yfinance and, for financial statements, Financial Modeling
Prep as a secondary source.  The CSV is overwritten and metadata updated with
the new ``source`` and ``fetched_at`` timestamp.  Any remaining ``ERROR``
entries are later handled by :mod:`fallback_data`.
"""

import json
from pathlib import Path

from modules.config_utils import get_output_dir, add_fmp_api_key

import pandas as pd
import yfinance as yf
import requests

from .utils import iso_timestamp_utc

# Base URL for Financial Modeling Prep (used only as fallback for statements)
FMP_BASE = "https://financialmodelingprep.com/api/v3"


def fetch_profile_from_yf(symbol: str) -> pd.DataFrame:
    """
    Fetch company profile using yfinance: we construct a DataFrame
    with columns similar to profile.csv from report_generator.py.
    """
    ticker = yf.Ticker(symbol)
    info = {}
    try:
        info = ticker.info or {}
    except Exception:
        info = {}

    # If yfinance.info is empty or missing longName, try FMP for profile
    if not info or info.get("longName") is None:
        # Fallback to FMP
        url = add_fmp_api_key(f"{FMP_BASE}/profile/{symbol}")
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if not data or not isinstance(data, list) or not data[0].get("companyName"):
            raise ValueError(f"No profile data available from yfinance or FMP for {symbol}")
        row = data[0]
        info = {
            "symbol": row.get("symbol", ""),
            "longName": row.get("companyName", ""),
            "sector": row.get("sector", ""),
            "industry": row.get("industry", ""),
            "marketCap": row.get("mktCap", pd.NA),
            "website": row.get("website", ""),
            # The rest of the columns can be left blank or filled as needed
        }

    # Build a one-row DataFrame matching the columns in report_generator.py
    columns = [
        "symbol", "price", "beta", "volAvg", "mktCap", "lastDiv", "range",
        "changes", "exchange", "industry", "website", "description", "ceo",
        "sector", "country", "fullTimeEmployees", "phone", "address", "city",
        "state", "zip", "dcfDiff", "dcf", "image"
    ]
    # Fill with actual keys when present, else blank/NA
    row_dict = {col: "" for col in columns}
    row_dict["symbol"] = symbol
    row_dict["industry"] = info.get("industry", "")
    row_dict["website"] = info.get("website", "")
    row_dict["sector"] = info.get("sector", "")
    row_dict["mktCap"] = info.get("marketCap", "")
    row_dict["price"] = info.get("currentPrice", "") or info.get("regularMarketPrice", "")
    row_dict["beta"] = info.get("beta", "")
    row_dict["volAvg"] = info.get("volumeAverage", "")
    row_dict["lastDiv"] = info.get("dividendRate", "")
    # description, ceo, etc. often not provided by yfinance.info; leave blank
    return pd.DataFrame([row_dict])


def fetch_1mo_prices_yf(symbol: str) -> pd.DataFrame:
    """
    Fetch 1‐month price history via yfinance (history). Returns a DataFrame
    with Date, Open, High, Low, Close, Adj Close, Volume.
    """
    ticker = yf.Ticker(symbol)
    try:
        hist = ticker.history(period="1mo")
    except Exception as e:
        raise RuntimeError(f"yfinance.history error: {e}")

    if hist is None or hist.empty or "Close" not in hist.columns:
        # Try yf.download() as fallback
        try:
            hist = yf.download(symbol, period="1mo")
        except Exception as e:
            raise RuntimeError(f"yf.download error: {e}")

    if hist is None or hist.empty:
        raise ValueError("No 1‐month price data available from yfinance.")

    # Drop unwanted columns
    hist = hist.drop(columns=[c for c in ("Dividends", "Stock Splits") if c in hist.columns])
    hist.reset_index(inplace=True)  # Make 'Date' a column again

    # Ensure expected columns are present; some sources may miss 'Adj Close'
    if "Adj Close" not in hist.columns and "Close" in hist.columns:
        hist["Adj Close"] = hist["Close"]

    desired_cols = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
    return hist.loc[:, [c for c in desired_cols if c in hist.columns]]


def fetch_fin_stmt_from_yf(symbol: str, stmt_key: str) -> pd.DataFrame:
    """
    Given symbol and a yfinance attribute name (e.g. 'financials', 'quarterly_financials',
    'balance_sheet', etc.), attempt to pull that DataFrame. Returns empty DataFrame
    if nothing is returned. The caller will decide if fallback to FMP is needed.
    """
    ticker = yf.Ticker(symbol)
    try:
        df = getattr(ticker, stmt_key)
        if not isinstance(df, pd.DataFrame):
            df = pd.DataFrame()
    except Exception:
        df = pd.DataFrame()

    if not isinstance(df, pd.DataFrame) or df.empty:
        return pd.DataFrame()

    return df.copy()


def fetch_fmp_statement(symbol: str, stmt_endpoint: str, period: str) -> pd.DataFrame:
    """
    stmt_endpoint: 'income-statement', 'balance-sheet-statement', or 'cash-flow-statement'.
    period: 'annual' or 'quarter' 
    """
    url = add_fmp_api_key(f"{FMP_BASE}/{stmt_endpoint}/{symbol}?period={period}")
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if not data or not isinstance(data, list):
        raise ValueError(f"No FMP data for {symbol} ({stmt_endpoint}, {period})")
    df = pd.DataFrame(data)
    # Use 'date' or 'period' as index if present
    if "date" in df.columns:
        df.set_index("date", inplace=True)
    elif "period" in df.columns:
        df.set_index("period", inplace=True)
    return df


def enrich_ticker_folder(ticker_dir: Path):
    """
    Examine metadata.json in ticker_dir, find any file entries whose 'source'
    starts with 'ERROR', and re-fetch them via yfinance (or FMP fallback).
    Overwrite the corresponding CSV, then update metadata.json accordingly.
    """
    meta_path = ticker_dir / "metadata.json"
    if not meta_path.is_file():
        print(f"  [WARN] No metadata.json in {ticker_dir.name}, skipping.")
        return

    with open(meta_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    files_meta = metadata.get("files", {})
    updated = False

    for filename, fileinfo in files_meta.items():
        source = fileinfo.get("source", "")
        if not source.startswith("ERROR"):
            # Nothing to fix for this file
            continue

        print(f"\n  ↻ Re-fetching '{filename}' for {ticker_dir.name} (was ERROR)...")
        symbol = ticker_dir.name.upper()
        new_source = None
        new_source_url = ""
        new_fetched = iso_timestamp_utc()
        csv_path = ticker_dir / filename

        try:
            if filename == "profile.csv":
                df = fetch_profile_from_yf(symbol)
                df.to_csv(csv_path, index=False)
                new_source = "yfinance / FMP (profile fallback)"
                new_source_url = f"https://finance.yahoo.com/quote/{symbol}/profile"
                print("    • Company profile re-fetched via yfinance/FMP.")

            elif filename == "1mo_prices.csv":
                df = fetch_1mo_prices_yf(symbol)
                df.to_csv(csv_path, index=False)
                new_source = "yfinance.history"
                new_source_url = f"https://finance.yahoo.com/quote/{symbol}/history?p={symbol}"
                print("    • 1‐month price history re-fetched via yfinance.")

            elif filename.endswith("_annual.csv") or filename.endswith("_quarter.csv"):
                # Determine which statement and whether annual/quarter.
                # Example filenames: 'income_annual.csv', 'income_quarter.csv', etc.
                key = filename.replace(".csv", "")  # e.g. 'income_annual'
                parts = key.split("_")
                stmt = parts[0]  # income, balance, or cash
                period = parts[1]  # 'annual' or 'quarter'

                # Map to yfinance attribute names:
                # income → 'financials' or 'quarterly_financials'
                # balance → 'balance_sheet' or 'quarterly_balance_sheet'
                # cash → 'cashflow' or 'quarterly_cashflow'
                if stmt == "income":
                    yf_attr = "financials" if period == "annual" else "quarterly_financials"
                    fmp_endpoint = "income-statement"
                elif stmt == "balance":
                    yf_attr = "balance_sheet" if period == "annual" else "quarterly_balance_sheet"
                    fmp_endpoint = "balance-sheet-statement"
                elif stmt == "cash":
                    yf_attr = "cashflow" if period == "annual" else "quarterly_cashflow"
                    fmp_endpoint = "cash-flow-statement"
                else:
                    raise ValueError(f"Unknown financial statement type in '{filename}'")

                # Try yfinance first
                df_yf = fetch_fin_stmt_from_yf(symbol, yf_attr)
                if not df_yf.empty:
                    # If columns are timestamps, transpose so index is date
                    should_transpose = any(isinstance(col, pd.Timestamp) for col in df_yf.columns)
                    df_to_save = df_yf.T if should_transpose else df_yf
                    df_to_save.to_csv(csv_path, index=True)
                    new_source = f"yfinance.{yf_attr}"
                    new_source_url = f"https://finance.yahoo.com/quote/{symbol}/financials"
                    if stmt == "balance":
                        new_source_url = f"https://finance.yahoo.com/quote/{symbol}/balance-sheet"
                    elif stmt == "cash":
                        new_source_url = f"https://finance.yahoo.com/quote/{symbol}/cash-flow"
                    print(f"    • {stmt.title()} ({period}) re-fetched via yfinance.")

                else:
                    # Fallback to FMP
                    df_fmp = fetch_fmp_statement(symbol, fmp_endpoint, period)
                    if df_fmp.empty:
                        raise ValueError(f"No FMP data for {filename}")
                    df_fmp.to_csv(csv_path, index=True)
                    new_source = f"FMP ({fmp_endpoint}, {period})"
                    new_source_url = f"{FMP_BASE}/{fmp_endpoint}/{symbol}"
                    print(f"    • {stmt.title()} ({period}) re-fetched via FMP.")

            elif filename == "report.md":
                # We do not regenerate the entire markdown here. Skip.
                print("    • Skipping report.md – needs to be manually regenerated via report_generator.py.")
                continue

            else:
                # Unknown filename; skip
                print(f"    • Unrecognized file '{filename}', skipping.")
                continue

            # Update metadata for this file
            files_meta[filename]["source"] = new_source
            files_meta[filename]["source_url"] = new_source_url
            files_meta[filename]["fetched_at"] = new_fetched
            updated = True

        except Exception as e:
            print(f"    ⚠ Failed to re-fetch '{filename}': {e}")
            # Leave the ERROR as-is (or append details)
            continue

    if updated:
        # Write back metadata.json
        metadata["files"] = files_meta
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        print(f"\n  ✓ Updated metadata.json for {ticker_dir.name}")
    else:
        print(f"\n  • No updates made for {ticker_dir.name} (no ERROR entries found).")


def run_for_tickers(tickers, output_root: str | None = None):
    """Run metadata enrichment only for the specified ticker list."""
    project_root = Path(__file__).resolve().parents[2]
    if output_root is None:
        output_root = str(get_output_dir())
    out_root = project_root / output_root if not Path(output_root).is_absolute() else Path(output_root)

    if not out_root.exists() or not out_root.is_dir():
        print(f"[ERROR] '{out_root}' does not exist or is not a directory.")
        return

    tickers = [t.upper() for t in tickers]
    print(
        f"\n[Metadata Enricher] Scanning {len(tickers)} ticker folder(s) under '{out_root}':\n"
    )
    for tk in tickers:
        dir_path = out_root / tk
        if dir_path.is_dir():
            print(f"→ Processing folder: {tk}")
            enrich_ticker_folder(dir_path)
        else:
            print(f"[WARN] Folder for '{tk}' not found under {out_root}.")

    print("\n[Metadata Enricher] Done.\n")


def main(output_root: str | None = None):
    project_root = Path(__file__).resolve().parents[2]
    if output_root is None:
        output_root = str(get_output_dir())
    output_root = project_root / output_root if not Path(output_root).is_absolute() else Path(output_root)

    if not output_root.exists() or not output_root.is_dir():
        print(f"[ERROR] '{output_root}' does not exist or is not a directory.")
        return

    subdirs = sorted([d for d in output_root.iterdir() if d.is_dir()])
    if not subdirs:
        print(f"[INFO] No subfolders under '{output_root}'. Nothing to do.")
        return

    print(f"\n[Metadata Enricher] Scanning {len(subdirs)} ticker folder(s) under '{output_root}':\n")
    for ticker_dir in subdirs:
        print(f"→ Processing folder: {ticker_dir.name}")
        enrich_ticker_folder(ticker_dir)

    print("\n[Metadata Enricher] Done.\n")


if __name__ == "__main__":
    main()
