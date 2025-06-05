# src/generate_report/fallback_data.py

"""Final safety net for repairing ticker folders.

If after running :mod:`metadata_checker` some files are still missing or contain
``ERROR`` entries, ``fallback_data.py`` performs a full yfinance download of
profile, price history and all statements.  The freshly fetched files replace
any incomplete ones and ``metadata.json`` is updated accordingly.

Usage example::

    run_fallback_data()  # scans output/, attempts fix for each ticker folder
"""

import json
import os
from pathlib import Path
from typing import Tuple

from modules.config_utils import get_output_dir, add_fmp_api_key

import pandas as pd
import requests
import yfinance as yf

from .utils import iso_timestamp_utc

FMP_BASE = "https://financialmodelingprep.com/api/v3"


#
# ─── Step 1: Define fallback helpers: yfinance full-fetch (fetch_and_display) ─────────────────────
#

def yf_full_fetch(symbol: str):
    """
    A “full” fallback that uses yfinance to retrieve Profile, 1-month price history,
    and all four financial statements. Writes files into output/<symbol>/.
    """
    symbol = symbol.upper()
    print(f"\n=== YF Fallback: Processing {symbol} ===")

    # Ensure output/<symbol>/ exists
    project_root = Path(__file__).resolve().parents[2]
    output_dir = project_root / "output" / symbol
    os.makedirs(output_dir, exist_ok=True)

    ticker = yf.Ticker(symbol)

    # 1) Company Info (profile.csv)
    try:
        info = ticker.info or {}
    except Exception as e:
        print(f"  Error fetching profile info via yfinance: {e}")
        info = {}

    if not info or info.get("longName") is None:
        print(f"  No profile info available via yfinance for {symbol}.")
    else:
        print(f"  Long Name : {info.get('longName')}")
        print(f"  Sector    : {info.get('sector')}")
        print(f"  Industry  : {info.get('industry')}")
        mc = info.get("marketCap")
        if isinstance(mc, (int, float)):
            print(f"  Market Cap: {mc:,}")
        else:
            print(f"  Market Cap: {mc}")
        print(f"  Website   : {info.get('website')}")

        # Build a minimal profile DataFrame
        profile_df = pd.DataFrame([{
            "symbol": symbol,
            "longName": info.get("longName", ""),
            "sector": info.get("sector", ""),
            "industry": info.get("industry", ""),
            "marketCap": info.get("marketCap", pd.NA),
            "website": info.get("website", "")
        }])
        profile_path = output_dir / "profile.csv"
        profile_df.to_csv(profile_path, index=False)
        print(f"  → Saved profile.csv to: {profile_path}")

    # 2) Recent Price History (1mo_prices.csv)
    try:
        hist = ticker.history(period="1mo")
    except Exception as e:
        print(f"  Error fetching price history via ticker.history(): {e}")
        hist = pd.DataFrame()

    if hist is None or hist.empty or "Close" not in hist.columns:
        print("  No 1-month price data from ticker.history; trying yf.download()...")
        try:
            hist = yf.download(symbol, period="1mo")
        except Exception as e:
            print(f"  Error fetching price via yf.download(): {e}")
            hist = pd.DataFrame()

    if hist is None or hist.empty:
        print(f"  No price history available for {symbol}.")
    else:
        df_price = hist.copy()
        # Drop unwanted columns if present
        for col in ("Dividends", "Stock Splits"):
            if col in df_price.columns:
                df_price = df_price.drop(columns=[col])

        print("\n  Last 5 rows of price history (1 month):")
        print(df_price.tail(5).to_string())

        # Save to CSV (include Date column)
        if "Adj Close" not in df_price.columns and "Close" in df_price.columns:
            df_price["Adj Close"] = df_price["Close"]

        df_price_reset = df_price.reset_index()
        price_csv_path = output_dir / "1mo_prices.csv"
        df_price_reset.to_csv(price_csv_path, index=False)
        print(f"  → Saved 1-month price history to: {price_csv_path}")

    # 3) Annual & Quarterly Financial Statements via yfinance
    _yf_fetch_and_save_statement(ticker, symbol, "financials", "Annual Income Statement", output_dir)
    _yf_fetch_and_save_statement(ticker, symbol, "quarterly_financials", "Quarterly Income Statement", output_dir)
    _yf_fetch_and_save_statement(ticker, symbol, "balance_sheet", "Annual Balance Sheet", output_dir)
    _yf_fetch_and_save_statement(ticker, symbol, "quarterly_balance_sheet", "Quarterly Balance Sheet", output_dir)
    _yf_fetch_and_save_statement(ticker, symbol, "cashflow", "Annual Cash Flow", output_dir)
    _yf_fetch_and_save_statement(ticker, symbol, "quarterly_cashflow", "Quarterly Cash Flow", output_dir)


def _yf_fetch_and_save_statement(
    ticker_obj: yf.Ticker,
    symbol: str,
    statement: str,
    label: str,
    output_dir: Path
):
    """
    Use yfinance to fetch `statement` DataFrame (e.g. 'financials', 'balance_sheet', etc.).
    If non-empty, transpose if necessary and save to CSV under output_dir/<symbol>_<statement>.csv.
    """
    try:
        df = getattr(ticker_obj, statement)
        if not isinstance(df, pd.DataFrame):
            df = pd.DataFrame()
    except Exception as e:
        print(f"\n  Error fetching {label} via yfinance: {e}")
        return

    if isinstance(df, pd.DataFrame) and not df.empty:
        print(f"\n  {label} (first 3 rows):")
        print(df.head(3).to_string())

        # Determine whether to transpose (if columns are date-like)
        try:
            if any(isinstance(col, pd.Timestamp) for col in df.columns):
                df_to_save = df.T
            else:
                df_to_save = df
        except Exception:
            df_to_save = df

        filename = f"{symbol}_{statement}.csv"
        filepath = output_dir / filename
        df_to_save.to_csv(filepath, index=True)
        print(f"  → Saved {label} to: {filepath}")
    else:
        print(f"\n  {label} not available or empty for {symbol}.")


#
# ─── Step 2: Define FMP-based fallback helpers ────────────────────────────────────────────────────
#

def fetch_profile_from_fmp(symbol: str) -> pd.DataFrame:
    """
    Fetch company profile from Financial Modeling Prep. Returns a DataFrame with
    at least these columns: symbol, longName, sector, industry, marketCap, website.
    Raises ValueError if no data is returned.
    """
    url = add_fmp_api_key(f"{FMP_BASE}/profile/{symbol}")
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if not data or not isinstance(data, list) or not data[0].get("companyName"):
        raise ValueError(f"No FMP profile data for {symbol}")
    row = data[0]
    df = pd.DataFrame([{
        "symbol": row.get("symbol", ""),
        "longName": row.get("companyName", ""),
        "sector": row.get("sector", ""),
        "industry": row.get("industry", ""),
        "marketCap": row.get("mktCap", pd.NA),
        "website": row.get("website", "")
    }])
    return df


def fetch_1mo_prices_fmp(symbol: str) -> pd.DataFrame:
    """Fetch 1-month daily price history from FMP."""
    url = add_fmp_api_key(
        f"{FMP_BASE}/historical-price-full/{symbol}?timeseries=30"
    )
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    hist = data.get("historical") if isinstance(data, dict) else None
    if not hist:
        raise ValueError(f"No FMP price data for {symbol}")
    df = pd.DataFrame(hist)
    rename_map = {
        "date": "Date",
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "adjClose": "Adj Close",
        "volume": "Volume",
    }
    df = df.rename(columns=rename_map)
    if "Adj Close" not in df.columns and "Close" in df.columns:
        df["Adj Close"] = df["Close"]
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    cols = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
    return df.loc[:, [c for c in cols if c in df.columns]]


def fetch_fmp_statement(symbol: str, stmt_endpoint: str, period: str) -> pd.DataFrame:
    """
    Fetch financial statement from FMP. stmt_endpoint e.g. 'income-statement',
    'balance-sheet-statement', 'cash-flow-statement'. Period: 'annual' or 'quarter'.
    Returns a DataFrame indexed by date if successful; raises ValueError otherwise.
    """
    url = add_fmp_api_key(f"{FMP_BASE}/{stmt_endpoint}/{symbol}?period={period}")
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if not data or not isinstance(data, list):
        raise ValueError(f"No FMP {stmt_endpoint} data for {symbol} ({period})")
    df = pd.DataFrame(data)
    if "date" in df.columns:
        df.set_index("date", inplace=True)
    elif "period" in df.columns:
        df.set_index("period", inplace=True)
    return df


#
# ─── Helper functions for targeted re-fetches ──────────────────────────────────
#

def _update_metadata_entry(files_meta: dict, filename: str, source: str, source_url: str, fetched: str) -> None:
    """Update metadata dictionary for ``filename``."""

    files_meta[filename]["source"] = source
    files_meta[filename]["source_url"] = source_url
    files_meta[filename]["fetched_at"] = fetched


def _parse_statement_filename(filename: str) -> tuple[str, str, str, str, str]:
    """Return statement info from ``filename``."""

    stmt, period = filename.replace(".csv", "").split("_")
    stmt_map = {
        "income": ("financials", "income-statement", "financials"),
        "balance": ("balance_sheet", "balance-sheet-statement", "balance-sheet"),
        "cash": ("cashflow", "cash-flow-statement", "cash-flow"),
    }
    if stmt not in stmt_map:
        raise ValueError(f"Unknown financial statement type in '{filename}'")
    yf_attr, fmp_endpoint, yahoo_path = stmt_map[stmt]
    yahoo_url = f"https://finance.yahoo.com/quote/{{symbol}}/{yahoo_path}"
    return stmt, period, yf_attr, fmp_endpoint, yahoo_url


def _re_fetch_profile(symbol: str, csv_path: Path) -> tuple[str, str]:
    """Fetch profile via FMP with yfinance fallback."""

    try:
        df = fetch_profile_from_fmp(symbol)
        df.to_csv(csv_path, index=False)
        print("    • Company profile re-fetched from FMP.")
        return "FMP (profile)", f"{FMP_BASE}/profile/{symbol}"
    except Exception:
        print("    • FMP profile failed; trying yfinance directly…")
        ticker = yf.Ticker(symbol)
        try:
            info = ticker.info or {}
            if info.get("longName") is None:
                raise ValueError("yfinance.info returned no profile.")
            profile_df = pd.DataFrame([
                {
                    "symbol": symbol,
                    "longName": info.get("longName", ""),
                    "sector": info.get("sector", ""),
                    "industry": info.get("industry", ""),
                    "marketCap": info.get("marketCap", pd.NA),
                    "website": info.get("website", ""),
                }
            ])
            profile_df.to_csv(csv_path, index=False)
            print("    • Company profile re-fetched from yfinance.")
            return "yfinance.profile", f"https://finance.yahoo.com/quote/{symbol}/profile"
        except Exception as exc:
            raise RuntimeError(f"Neither FMP nor yfinance profile succeeded: {exc}") from exc


def _re_fetch_prices(symbol: str, csv_path: Path) -> tuple[str, str]:
    """Fetch one month of prices via yfinance."""

    try:
        hist = yf.Ticker(symbol).history(period="1mo")
        if hist is None or hist.empty or "Close" not in hist.columns:
            raise ValueError("No data in ticker.history()")
        df_price = hist.drop(columns=[c for c in ("Dividends", "Stock Splits") if c in hist.columns])
        if "Adj Close" not in df_price.columns and "Close" in df_price.columns:
            df_price["Adj Close"] = df_price["Close"]
        df_price.reset_index().to_csv(csv_path, index=False)
        print("    • 1‐month price history re-fetched from yfinance.")
        return "yfinance.history", f"https://finance.yahoo.com/quote/{symbol}/history?p={symbol}"
    except Exception as exc:
        raise RuntimeError(f"Failed to fetch 1mo_prices via yfinance: {exc}") from exc


def _re_fetch_statement(symbol: str, filename: str, csv_path: Path) -> tuple[str, str]:
    """Fetch financial statement using yfinance with FMP fallback."""

    stmt, period, yf_attr, fmp_endpoint, yahoo_url = _parse_statement_filename(filename)
    df_yf = getattr(yf.Ticker(symbol), yf_attr)
    if not isinstance(df_yf, pd.DataFrame):
        df_yf = pd.DataFrame()
    if not df_yf.empty:
        should_transpose = any(isinstance(col, pd.Timestamp) for col in df_yf.columns)
        df_to_save = df_yf.T if should_transpose else df_yf
        df_to_save.to_csv(csv_path, index=True)
        print(f"    • {stmt.title()} ({period}) re-fetched from yfinance.")
        return f"yfinance.{yf_attr}", yahoo_url.format(symbol=symbol)

    df_fmp = fetch_fmp_statement(symbol, fmp_endpoint, period)
    if df_fmp.empty:
        raise ValueError(f"No FMP data for {filename}")
    df_fmp.to_csv(csv_path, index=True)
    print(f"    • {stmt.title()} ({period}) re-fetched from FMP.")
    return f"FMP ({fmp_endpoint}, {period})", f"{FMP_BASE}/{fmp_endpoint}/{symbol}"


#
# ─── Step 3: Per-file “repair” logic ────────────────────────────────────────────────────────────────
#

def enrich_ticker_folder(ticker_dir: Path):
    """
    1. Load metadata.json for this ticker.
    2. For each file with source.startswith("ERROR"), attempt a targeted re-fetch:
         - For profile.csv: try FMP->DataFrame
         - For 1mo_prices.csv: try yfinance.history
         - For <stmt>_annual.csv or _quarter.csv: try yfinance.<stmt> or fallback to FMP
    3. If any single-file fetch still fails, run yf_full_fetch(symbol) to recreate all CSVs.
    4. Update metadata.json with new 'source', 'source_url', and 'fetched_at'.
    """
    meta_path = ticker_dir / "metadata.json"
    if not meta_path.is_file():
        print(f"  [WARN] No metadata.json in {ticker_dir.name}, skipping.")
        return

    with open(meta_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    files_meta = metadata.get("files", {})
    updated = False
    any_errors = False
    for filename, fileinfo in files_meta.items():
        source = fileinfo.get("source", "")
        if not source.startswith("ERROR"):
            continue

        print(f"\n  ↻ Re-fetching '{filename}' for {ticker_dir.name} (was ERROR)...")
        symbol = ticker_dir.name.upper()
        csv_path = ticker_dir / filename
        new_fetched = iso_timestamp_utc()

        try:
            if filename == "profile.csv":
                new_source, new_source_url = _re_fetch_profile(symbol, csv_path)

            elif filename == "1mo_prices.csv":
                new_source, new_source_url = _re_fetch_prices(symbol, csv_path)

            elif filename.endswith("_annual.csv") or filename.endswith("_quarter.csv"):
                new_source, new_source_url = _re_fetch_statement(symbol, filename, csv_path)

            elif filename == "report.md":
                print("    • Skipping report.md (needs manual re-run of report_generator).")
                continue

            else:
                print(f"    • Unrecognized file '{filename}', skipping.")
                continue

            _update_metadata_entry(files_meta, filename, new_source, new_source_url, new_fetched)
            updated = True
        except Exception as e:
            print(f"    ⚠ Failed to re-fetch '{filename}': {e}")
            any_errors = True
            continue

    # ─── If any single-file fetch failed, run a full yfinance fallback ─────────────────────────────
    if any_errors:
        symbol = ticker_dir.name.upper()
        print(f"\n  ▶ Some files still failed for {symbol}; running full YF fallback…")
        try:
            yf_full_fetch(symbol)
            print(f"    • yf_full_fetch({symbol}) completed.")
        except Exception as e:
            print(f"    ⚠ Full YF fallback also failed for {symbol}: {e}")
        else:
            # Now that we re-ran yf_full_fetch, update any remaining ERROR entries in metadata
            new_ts = iso_timestamp_utc()
            for fn in files_meta:
                if files_meta[fn].get("source", "").startswith("ERROR"):
                    files_meta[fn]["source"] = "yfinance-full-fallback"
                    files_meta[fn]["source_url"] = ""
                    files_meta[fn]["fetched_at"] = new_ts
            updated = True

    # ─── Write back metadata.json if we updated anything ──────────────────────────────────────────
    if updated:
        metadata["files"] = files_meta
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        print(f"\n  ✓ Updated metadata.json for {ticker_dir.name}")
    else:
        print(f"\n  • No changes made for {ticker_dir.name}.")


#
# ─── Step 4: Directory scan entry point ───────────────────────────────────────────────────────────
#

def run_fallback_data(tickers=None, output_root: str | None = None):
    """Run fallback enrichment for all or selected tickers."""
    project_root = Path(__file__).resolve().parents[2]
    if output_root is None:
        output_root = str(get_output_dir())
    output_root = project_root / output_root if not Path(output_root).is_absolute() else Path(output_root)

    if not output_root.exists() or not output_root.is_dir():
        print(f"[ERROR] '{output_root}' does not exist or is not a directory.")
        return

    if tickers is None:
        subdirs = sorted([d for d in output_root.iterdir() if d.is_dir()])
    else:
        subdirs = [(output_root / t.upper()) for t in tickers]

    if not subdirs:
        print(f"[INFO] No subdirectories under '{output_root}'. Nothing to do.")
        return

    print(f"\n[Fallback Data] Scanning {len(subdirs)} ticker folder(s) under '{output_root}':\n")
    for ticker_dir in subdirs:
        if ticker_dir.is_dir():
            print(f"→ Processing folder: {ticker_dir.name}")
            enrich_ticker_folder(ticker_dir)
        else:
            print(f"[WARN] Folder '{ticker_dir}' not found.")

    print("\n[Fallback Data] Done.\n")
