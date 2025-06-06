"""Simple CLI portfolio manager backed by Directus."""

from __future__ import annotations

import os

from modules.analytics import portfolio_summary, sector_counts
from modules.interface import (
    print_table,
    print_invalid_choice,
    print_header,
    print_menu,
)

import pandas as pd
from modules.data.term_mapper import resolve_term
from modules.data.directus_client import fetch_items, insert_items
from modules.data import prepare_records
C_DIRECTUS_COLLECTION = os.getenv("DIRECTUS_PORTFOLIO_COLLECTION", "portfolio")
COLUMNS = [
    "Ticker",
    "Name",
    "Sector",
    "Industry",
    "Current Price",
    "Market Cap",
    "PE Ratio",
    "Dividend Yield",
]

NUMERIC_FIELDS = {
    "Current Price",
    "Market Cap",
    "PE Ratio",
    "Dividend Yield",
}

# Mapping of Directus field names to our dataframe columns when reading
FROM_DIRECTUS = {
    "ticker": "Ticker",
    "ticker_symbol": "Ticker",
    "name": "Name",
    "company_name": "Name",
    "sector": "Sector",
    "industry": "Industry",
    "current_price": "Current Price",
    "market_cap": "Market Cap",
    "pe_ratio": "PE Ratio",
    "dividend_yield": "Dividend Yield",
}


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure DataFrame has expected columns and no completely empty rows."""
    for col in COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA
    df = df.dropna(how="all")
    if "Ticker" in df.columns:
        df = df[df["Ticker"].notna()]
    return df[COLUMNS]


def _append_row(df: pd.DataFrame, data: dict) -> pd.DataFrame:
    """Return ``df`` with ``data`` appended as a new row."""
    new_row = pd.DataFrame([data], columns=COLUMNS)
    if df.empty:
        return new_row
    return pd.concat([df, new_row], ignore_index=True)


def _load_from_directus() -> pd.DataFrame:
    """Return portfolio data loaded from Directus."""
    records = fetch_items(C_DIRECTUS_COLLECTION)
    if not records:
        return pd.DataFrame(columns=COLUMNS)
    df = pd.DataFrame(records).rename(columns=FROM_DIRECTUS)
    return _clean_dataframe(df)


def _save_to_directus(df: pd.DataFrame) -> None:
    """Persist portfolio data to Directus."""
    records = prepare_records(C_DIRECTUS_COLLECTION, df.to_dict(orient="records"))
    insert_items(C_DIRECTUS_COLLECTION, records)


def load_portfolio() -> pd.DataFrame:
    """Return portfolio data from Directus or an empty DataFrame."""
    try:
        return _load_from_directus()
    except Exception as exc:  # pragma: no cover - network failure
        print(f"Error loading portfolio from Directus: {exc}")
        return pd.DataFrame(columns=COLUMNS)


def save_portfolio(df: pd.DataFrame) -> None:
    """Persist the portfolio DataFrame to Directus."""
    try:
        _save_to_directus(df)
    except Exception as exc:  # pragma: no cover - network failure
        print(f"Error saving portfolio to Directus: {exc}")


def prompt_manual_entry(ticker: str) -> dict:
    """
    Prompt the user to manually fill out each field for a given ticker.
    Returns a dict mapping column names to user-provided values.
    """
    print(f"\nPlease fill out data for {ticker} manually.")
    data = {"Ticker": ticker.upper()}
    for field in COLUMNS[1:]:
        val = input(f"  {field}: ").strip()
        if field in NUMERIC_FIELDS:
            try:
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


def fetch_from_unified(ticker: str, *, use_openbb: bool | None = None) -> dict:
    """Return company data via the unified fetcher."""
    from modules.data.unified_fetcher import fetch_company_data

    data = fetch_company_data(ticker, use_openbb=use_openbb)
    if data is None:
        raise ValueError("Data not found")
    return data


def confirm_or_adjust_ticker(original: str) -> str:
    """
    If automated fetching fails, ask the user to confirm the ticker symbol.
    If confirmed incorrect, prompt for a replacement.
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


def ticker_exists(df: pd.DataFrame, tk: str) -> bool:
    """Return True if the ticker already exists in the portfolio."""
    existing = df["Ticker"].dropna().astype(str).values
    return tk in existing


def add_tickers(portfolio: pd.DataFrame) -> pd.DataFrame:
    """
    Prompt the user to enter one or more tickers to add. For each ticker:
    - Attempt to fetch data via :mod:`modules.data.unified_fetcher`.
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
        if ticker_exists(portfolio, tk):
            print(f"  → Ticker '{tk}' is already in your portfolio. Skipping.\n")
            continue

        while True:
            try:
                data = fetch_from_unified(tk)
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

        portfolio = _append_row(portfolio, data)
        print(f"  ✓ Added '{tk}' to portfolio.\n")

    return portfolio


def remove_ticker(portfolio: pd.DataFrame) -> pd.DataFrame:
    """
    Prompt the user for a ticker to remove from the portfolio.
    """
    tk = input("Enter the ticker symbol to remove (or press Enter to cancel): ").strip().upper()
    if not tk:
        print("Canceled.\n")
        return portfolio

    if not ticker_exists(portfolio, tk):
        print(f"  × Ticker '{tk}' not found in portfolio.\n")
    else:
        portfolio = portfolio[portfolio["Ticker"] != tk].reset_index(drop=True)
        print(f"  ✓ Removed '{tk}' from portfolio.\n")
    return portfolio


def update_tickers(portfolio: pd.DataFrame) -> pd.DataFrame:
    """Refresh data for each ticker via the unified fetcher."""
    if portfolio.empty:
        print("Portfolio is empty.\n")
        return portfolio

    for idx, row in portfolio.iterrows():
        tk = row["Ticker"]
        try:
            data = fetch_from_unified(tk)
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
    print_header("\U0001F4C8 Portfolio Manager")
    portfolio = load_portfolio()

    while True:
        print("Choose an action:")
        options = [
            "View portfolio",
            "Add ticker(s)",
            "Update ticker data",
            "Remove ticker",
            "Exit",
        ]
        print_menu(options)
        choice = input(f"Select an option [1-{len(options)}]: ").strip()

        if choice == "1":
            view_portfolio(portfolio)

        elif choice == "2":
            portfolio = add_tickers(portfolio)
            save_portfolio(portfolio)

        elif choice == "3":
            portfolio = update_tickers(portfolio)
            save_portfolio(portfolio)

        elif choice == "4":
            portfolio = remove_ticker(portfolio)
            save_portfolio(portfolio)

        elif choice == "5":
            print("Exiting Portfolio Manager.")
            break

        else:
            print_invalid_choice()


if __name__ == "__main__":
    main()
