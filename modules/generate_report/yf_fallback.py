# src/generate_report/yf_fallback.py

import yfinance as yf
import pandas as pd
import os
from pathlib import Path

def fetch_and_display(symbol: str):
    """
    1) Fetch basic company info and print selected fields.
    2) Download and print 1 month of price history.
    3) Fetch annual and quarterly financial statements and print/save them.
    This writes files into: <project_root>/output/<symbol>/
    """
    symbol = symbol.upper()
    print(f"\n=== YF Fallback: Processing {symbol} ===")

    # Make sure the CSVs go into output/<symbol>/ instead of src/output/
    project_root = Path(__file__).resolve().parents[2]
    output_dir = project_root / "output" / symbol
    os.makedirs(output_dir, exist_ok=True)

    ticker = yf.Ticker(symbol)

    # 1) Company Info
    try:
        info = ticker.info
    except Exception as e:
        print(f"  Error fetching info: {e}")
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

        # Save a minimal CSV profile
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
        print(f"  → Saved profile.csv to {profile_path}")

    # 2) Recent Price History (last 1 month)
    try:
        hist = ticker.history(period="1mo")
    except Exception as e:
        print(f"  Error fetching price history: {e}")
        hist = pd.DataFrame()

    if hist is None or hist.empty or "Close" not in hist.columns:
        print("  No 1-month price data via ticker.history; trying yf.download()...")
        try:
            hist = yf.download(symbol, period="1mo")
        except Exception as e:
            print(f"  Error on yf.download(): {e}")
            hist = pd.DataFrame()

    if hist is None or hist.empty:
        print(f"  No price history available for {symbol}.")
    else:
        hist_df = hist.copy()
        # Drop Dividends/Stock Splits if they exist
        for col in ["Dividends", "Stock Splits"]:
            if col in hist_df.columns:
                hist_df = hist_df.drop(columns=[col])

        print("\n  Last 5 rows of price history (1 month):")
        print(hist_df.tail(5).to_string())

        price_csv_path = output_dir / f"{symbol}_1mo_prices.csv"
        hist_df.reset_index().to_csv(price_csv_path, index=False)
        print(f"  → Saved 1-month price history to: {price_csv_path}")

    # 3) Annual & Quarterly Financial Statements
    _fetch_and_save_financial_statement(ticker, symbol, "financials", "Annual Income Statement", output_dir)
    _fetch_and_save_financial_statement(ticker, symbol, "quarterly_financials", "Quarterly Income Statement", output_dir)
    _fetch_and_save_financial_statement(ticker, symbol, "balance_sheet", "Annual Balance Sheet", output_dir)
    _fetch_and_save_financial_statement(ticker, symbol, "quarterly_balance_sheet", "Quarterly Balance Sheet", output_dir)
    _fetch_and_save_financial_statement(ticker, symbol, "cashflow", "Annual Cash Flow", output_dir)
    _fetch_and_save_financial_statement(ticker, symbol, "quarterly_cashflow", "Quarterly Cash Flow", output_dir)


def _fetch_and_save_financial_statement(ticker_obj, symbol: str, statement: str, label: str, output_dir: Path):
    """
    Attempts to fetch the DataFrame for `statement` via yfinance.
    If data is present, prints the top 3 rows and saves to CSV under output_dir/<symbol>_<statement>.csv.
    If empty or error, prints a message.
    """
    try:
        df = getattr(ticker_obj, statement)
    except Exception as e:
        print(f"\n  Error fetching {label}: {e}")
        return

    if isinstance(df, pd.DataFrame) and not df.empty:
        print(f"\n  {label} (first 3 rows):")
        print(df.head(3).to_string())

        # If columns are dates, transpose so rows are periods
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
