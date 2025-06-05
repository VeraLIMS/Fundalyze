"""
script: portfolio_manager.py

Dependencies:
    pip install yfinance pandas openpyxl

Usage:
    python portfolio_manager.py

Description:
    A simple CLI tool to manage a stock portfolio. You can:
    - Add tickers (automatically fetch key data via yfinance; if fetch fails, confirm/adjust ticker or enter data manually).
    - Remove tickers.
    - View current portfolio.
    - Data is persisted in an Excel file ("portfolio.xlsx") in the same directory.
"""

import os
import sys
from typing import Optional

from modules.analytics import portfolio_summary, sector_counts
from modules.interface import print_table, print_invalid_choice

import pandas as pd
import requests
from modules.data.term_mapper import resolve_term
from modules.data.directus_client import (
    fetch_items,
    insert_items,
    list_fields,
)

PORTFOLIO_FILE = "portfolio.xlsx"
C_DIRECTUS_COLLECTION = os.getenv("DIRECTUS_PORTFOLIO_COLLECTION", "portfolio")
USE_DIRECTUS = bool(os.getenv("DIRECTUS_URL"))
COLUMNS = [
    "Ticker",
    "Name",
    "Sector",
    "Industry",
    "Current Price",
    "Market Cap",
    "PE Ratio",
    "Dividend Yield"
]


def load_portfolio(filepath: str) -> pd.DataFrame:
    """
    Load the portfolio either from Directus (if configured) or from a local
    Excel file. If loading fails, an empty DataFrame with the expected columns
    is returned.
    """
    if USE_DIRECTUS:
        try:
            records = fetch_items(C_DIRECTUS_COLLECTION)
            if not records:
                return pd.DataFrame(columns=COLUMNS)
            df = pd.DataFrame(records)
            for col in COLUMNS:
                if col not in df.columns:
                    df[col] = pd.NA
            return df[COLUMNS]
        except Exception as exc:
            print(f"Error loading portfolio from Directus: {exc}")
            print("Falling back to local Excel file.")

    if os.path.isfile(filepath):
        try:
            df = pd.read_excel(filepath, engine="openpyxl")
            for col in COLUMNS:
                if col not in df.columns:
                    df[col] = pd.NA
            return df[COLUMNS]
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
    return pd.DataFrame(columns=COLUMNS)


def save_portfolio(df: pd.DataFrame, filepath: str):
    """
    Save the portfolio either to Directus (if configured) or to a local Excel
    file as fallback.
    """
    if USE_DIRECTUS:
        try:
            allowed = set(list_fields(C_DIRECTUS_COLLECTION))
            records = []
            for row in df.to_dict(orient="records"):
                filtered = {k: v for k, v in row.items() if k in allowed}
                records.append(filtered)
            insert_items(C_DIRECTUS_COLLECTION, records)
            print(
                f"→ Saved portfolio to Directus collection '{C_DIRECTUS_COLLECTION}'.\n"
            )
            return
        except Exception as exc:
            print(f"Error saving portfolio to Directus: {exc}")
            print("Falling back to local Excel file.")

    try:
        df.to_excel(filepath, index=False, engine="openpyxl")
        print(f"→ Saved portfolio to '{filepath}'.\n")
    except Exception as e:
        print(f"Error saving portfolio: {e}")

    # Also sync with Directus if environment variables are configured
    api_url = os.getenv("DIRECTUS_URL")
    token = os.getenv("DIRECTUS_TOKEN")
    if api_url and token:
        try:
            url = f"{api_url.rstrip('/')}/items/portfolio"
            headers = {"Authorization": f"Bearer {token}"}
            records = df.to_dict(orient="records")
            resp = requests.post(url, json=records, headers=headers, params={"upsert": "Ticker"})
            if resp.status_code >= 300:
                print(f"Warning syncing portfolio to Directus: {resp.status_code} {resp.text}")
            else:
                print("→ Synced portfolio to Directus.\n")
        except Exception as e:
            print(f"Error syncing portfolio to Directus: {e}")


def prompt_manual_entry(ticker: str) -> dict:
    """
    Prompt the user to manually fill out each field for a given ticker.
    Returns a dict mapping column names to user-provided values.
    """
    print(f"\nPlease fill out data for {ticker} manually.")
    data = {"Ticker": ticker.upper()}
    for field in COLUMNS[1:]:
        val = input(f"  {field}: ").strip()
        # Attempt to convert numeric fields to float if possible
        if field in ("Current Price", "Market Cap", "PE Ratio", "Dividend Yield"):
            try:
                # allow blank (treat as NaN) or numeric
                data[field] = float(val) if val else pd.NA
            except ValueError:
                data[field] = pd.NA
        else:
            data[field] = val if val else ""

    # Normalize sector/industry via term mapper
    if "Sector" in data:
        data["Sector"] = resolve_term(data["Sector"])
    if "Industry" in data:
        data["Industry"] = resolve_term(data["Industry"])
    return data


def fetch_from_yfinance(ticker: str) -> dict:
    """Wrapper around :func:`modules.data.fetching.fetch_basic_stock_data`."""
    from modules.data.fetching import fetch_basic_stock_data

    return fetch_basic_stock_data(ticker)


def confirm_or_adjust_ticker(original: str) -> str:
    """
    If yfinance fetch fails, ask the user: "Is this the correct ticker?"
    If yes, return the same string. If no, prompt for a new ticker and return it.
    """
    while True:
        resp = input(
            f"Ticker '{original}' not found or incomplete. Is this ticker correct? (Y/N): "
        ).strip().lower()
        if resp in ("y", "yes"):
            return original.upper()
        elif resp in ("n", "no"):
            new_ticker = input(
                "Enter the correct ticker symbol (or leave blank to cancel): "
            ).strip().upper()
            if not new_ticker:
                return ""
            return new_ticker
        else:
            print("  Please answer 'Y' or 'N'.")


def add_tickers(portfolio: pd.DataFrame) -> pd.DataFrame:
    """
    Prompt the user to enter one or more tickers to add. For each ticker:
    - Attempt to fetch data via yfinance.
    - If fetch fails or missing, confirm/adjust ticker or allow manual fill.
    - Append a new row to the portfolio DataFrame.
    """
    raw = input(
        "Enter ticker symbol(s) to add (comma-separated, or press Enter to cancel): "
    ).strip()
    if not raw:
        print("No tickers entered. Returning to main menu.\n")
        return portfolio

    tickers = [t.strip().upper() for t in raw.split(",") if t.strip()]
    for tk in tickers:
        # If ticker already in portfolio, skip it
        if tk in portfolio["Ticker"].values:
            print(f"  → Ticker '{tk}' is already in your portfolio. Skipping.\n")
            continue

        while True:
            try:
                data = fetch_from_yfinance(tk)
                print(f"  → Fetched data for {tk}:")
                print(f"      Name         : {data['Name']}")
                print(f"      Sector       : {data['Sector']}")
                print(f"      Industry     : {data['Industry']}")
                print(f"      Current Price: {data['Current Price']}")
                print(f"      Market Cap   : {data['Market Cap']}")
                print(f"      PE Ratio     : {data['PE Ratio']}")
                print(f"      Dividend Yld : {data['Dividend Yield']}")
                break  # successful fetch

            except Exception as e:
                print(f"  × Fetching '{tk}' failed: {e}")
                corrected = confirm_or_adjust_ticker(tk)
                if not corrected:
                    # User chose to cancel adding this ticker
                    print(f"  → Skipping '{tk}'\n")
                    data = None
                    break
                else:
                    tk = corrected  # retry with the new ticker

        if data is None:
            continue  # move on to next ticker

        # If fetch succeeded, but user might still want to override:
        override = input(
            "  Is this information correct? (Y to accept / N to fill manually): "
        ).strip().lower()
        if override in ("n", "no"):
            data = prompt_manual_entry(tk)

        # Append to portfolio DataFrame using pd.concat
        new_row = pd.DataFrame([data], columns=COLUMNS)
        if portfolio.empty:
            portfolio = new_row
        else:
            portfolio = pd.concat([portfolio, new_row], ignore_index=True)
        print(f"  ✓ Added '{tk}' to portfolio.\n")

    return portfolio


def remove_ticker(portfolio: pd.DataFrame) -> pd.DataFrame:
    """
    Prompt the user for a ticker to remove from the portfolio.
    """
    tk = input("Enter the ticker symbol to remove: ").strip().upper()
    if not tk:
        print("No ticker entered. Returning to main menu.\n")
        return portfolio

    if tk not in portfolio["Ticker"].values:
        print(f"  × Ticker '{tk}' not found in portfolio.\n")
    else:
        portfolio = portfolio[portfolio["Ticker"] != tk].reset_index(drop=True)
        print(f"  ✓ Removed '{tk}' from portfolio.\n")
    return portfolio


def update_tickers(portfolio: pd.DataFrame) -> pd.DataFrame:
    """Refresh data for each ticker via yfinance."""
    if portfolio.empty:
        print("Portfolio is empty.\n")
        return portfolio

    for idx, row in portfolio.iterrows():
        tk = row["Ticker"]
        try:
            data = fetch_from_yfinance(tk)
            for col in COLUMNS[1:]:
                portfolio.at[idx, col] = data.get(col, portfolio.at[idx, col])
            print(f"  ✓ Updated {tk}")
        except Exception as e:
            print(f"  × Could not update {tk}: {e}")

    return portfolio


def view_portfolio(portfolio: pd.DataFrame):
    """
    Display the current portfolio in a tabular format.
    """
    if portfolio.empty:
        print("Your portfolio is currently empty.\n")
        return

    print("\nCurrent Portfolio:")
    print_table(portfolio)
    summary = portfolio_summary(portfolio)
    if not summary.empty:
        print("\nSummary (mean/min/max):")
        print_table(summary, showindex=True)
    counts = sector_counts(portfolio)
    if not counts.empty:
        print("\nSectors:")
        print_table(counts)
    print("")


def main():
    print("\n=== Portfolio Manager ===\n")
    portfolio = load_portfolio(PORTFOLIO_FILE)

    while True:
        print("Choose an action:")
        print("  1) View portfolio")
        print("  2) Add ticker(s)")
        print("  3) Update ticker data")
        print("  4) Remove ticker")
        print("  5) Exit")
        choice = input("Enter 1/2/3/4/5: ").strip()

        if choice == "1":
            view_portfolio(portfolio)

        elif choice == "2":
            portfolio = add_tickers(portfolio)
            save_portfolio(portfolio, PORTFOLIO_FILE)

        elif choice == "3":
            portfolio = update_tickers(portfolio)
            save_portfolio(portfolio, PORTFOLIO_FILE)

        elif choice == "4":
            portfolio = remove_ticker(portfolio)
            save_portfolio(portfolio, PORTFOLIO_FILE)

        elif choice == "5":
            print("Exiting Portfolio Manager.")
            break

        else:
            print_invalid_choice()


if __name__ == "__main__":
    main()
