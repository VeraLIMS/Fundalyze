"""
script: group_analysis.py

Dependencies:
    pip install yfinance pandas

Usage:
    python src/group_analysis.py

Description:
    CLI tool to manage “groups” of stocks—e.g., those in the same sector or
    similar to a given portfolio holding. You can:
      - View existing groups and their members
      - Create a new group (optionally tied to a portfolio ticker)
      - Add tickers to a group (fetching key data via yfinance; manual override if necessary)
      - Remove tickers from a group
      - Delete an entire group
      - Link a group to a stock in your existing portfolio collection.
"""

import os

from modules.config_utils import load_settings  # noqa: E402
from modules.analytics import portfolio_summary
from modules.interface import (
    print_table,
    print_invalid_choice,
    print_header,
    print_menu,
)

SETTINGS = load_settings()

import pandas as pd
from modules.utils import parse_number
from modules.data.term_mapper import resolve_term
from modules.data.directus_client import fetch_items, insert_items
from modules.data import prepare_records

GROUPS_COLLECTION = os.getenv("DIRECTUS_GROUPS_COLLECTION", "groups")

# Columns used for each group entry (plus a "Group" column)
COLUMNS = [
    "Group",        # e.g. a portfolio ticker or custom group name
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

# Possible mapping of Directus field names to our expected columns
FROM_DIRECTUS = {
    "group": "Group",
    "ticker": "Ticker",
    "ticker_symbol": "Ticker",
    "company_name": "Name",
    "name": "Name",
    "sector": "Sector",
    "industry": "Industry",
    "current_price": "Current Price",
    "market_cap": "Market Cap",
    "pe_ratio": "PE Ratio",
    "dividend_yield": "Dividend Yield",
}


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure ``df`` contains the expected columns and remove empty rows."""
    for col in COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA
    df = df.dropna(how="all")
    if "Group" in df.columns:
        df = df[df["Group"].notna()]
    return df[COLUMNS]


def _load_from_directus() -> pd.DataFrame:
    """Return group data fetched from Directus."""
    records = fetch_items(GROUPS_COLLECTION)
    if not records:
        return pd.DataFrame(columns=COLUMNS)
    df = pd.DataFrame(records).rename(columns=FROM_DIRECTUS)
    return _clean_dataframe(df)

def load_portfolio() -> pd.DataFrame:
    """Return portfolio data from Directus."""
    from modules.management.portfolio_manager.portfolio_manager import load_portfolio as lp

    try:
        return lp()
    except Exception as exc:
        print(f"Error loading portfolio from Directus: {exc}")
        return pd.DataFrame()



def load_groups() -> pd.DataFrame:
    """Return existing groups from Directus."""
    try:
        return _load_from_directus()
    except Exception as exc:
        print(f"Error loading groups from Directus: {exc}")
        return pd.DataFrame(columns=COLUMNS)


def save_groups(df: pd.DataFrame) -> None:
    """Persist groups to Directus."""
    records = prepare_records(GROUPS_COLLECTION, df.to_dict(orient="records"))
    try:
        insert_items(GROUPS_COLLECTION, records)
    except Exception as exc:
        print(f"Error saving groups to Directus: {exc}")


def fetch_from_yfinance(ticker: str) -> dict:
    """Wrapper around :func:`modules.data.fetching.fetch_basic_stock_data`."""
    from modules.data.fetching import fetch_basic_stock_data

    return fetch_basic_stock_data(ticker)


def prompt_manual_entry(ticker: str) -> dict:
    """
    If automated fetch fails or user overrides, prompt manual entry.
    """
    print(f"\nPlease fill out data for '{ticker}' manually.")
    data = {"Ticker": ticker.upper()}
    for field in COLUMNS[2:]:  # skip "Group" and "Ticker"
        val = input(f"  {field}: ").strip()
        if field in NUMERIC_FIELDS:
            try:
                data[field] = parse_number(val) if val else pd.NA
                if isinstance(data[field], str):
                    data[field] = pd.NA
            except Exception:
                data[field] = pd.NA
        else:
            data[field] = val if val else ""

    if "Sector" in data:
        data["Sector"] = resolve_term(data["Sector"])
    if "Industry" in data:
        data["Industry"] = resolve_term(data["Industry"])
    return data


def confirm_or_adjust_ticker(original: str) -> str:
    """
    If yfinance fetch fails, ask: “Is this ticker correct?” If no, prompt new ticker.
    Return empty string to cancel.
    """
    while True:
        resp = input(
            f"Ticker '{original}' not found or incomplete. Is this ticker correct? (Y/N): "
        ).strip().lower()
        if resp in ("y", "yes"):
            return original.upper()
        elif resp in ("n", "no"):
            new_tk = input(
                "Enter the correct ticker symbol (or leave blank to cancel): "
            ).strip().upper()
            if not new_tk:
                return ""
            return new_tk
        else:
            print("  Please answer 'Y' or 'N'.")


def choose_group(portfolio: pd.DataFrame) -> str:
    """
    Ask user whether to link a new group to a portfolio ticker or create a custom name.
    """
    if not portfolio.empty:
        print("\nYou have the following portfolio tickers:")
        unique_ts = portfolio["Ticker"].dropna().unique().tolist()
        for i, t in enumerate(unique_ts, start=1):
            print(f"  {i}) {t}")
        print(f"  {len(unique_ts) + 1}) Create a custom group name")

        choice = input(
            f"Select 1-{len(unique_ts)+1} (or press Enter to cancel): "
        ).strip()
        if not choice:
            return ""
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(unique_ts):
                return unique_ts[idx - 1]  # use portfolio ticker as group name
            if idx == len(unique_ts) + 1:
                name = input("Enter custom group name (or press Enter to cancel): ").strip()
                return name if name else ""
    # If portfolio is empty or user skipped above
    name = input("Enter new group name (or press Enter to cancel): ").strip()
    return name if name else ""


def add_tickers_to_group(groups: pd.DataFrame, group_name: str) -> pd.DataFrame:
    """
    Prompt for tickers to add to a specific group. Fetch data, allow override.
    Append to 'groups' DataFrame under the given group_name.
    """
    raw = input(
        f"Enter ticker symbol(s) to add to group '{group_name}' (comma-separated, or press Enter to cancel): "
    ).strip()
    if not raw:
        print("No tickers entered. Returning to menu.\n")
        return groups

    tickers = [t.strip().upper() for t in raw.split(",") if t.strip()]
    for tk in tickers:
        # Check if (group_name, tk) already exists
        exists = ((groups["Group"] == group_name) & (groups["Ticker"] == tk)).any()
        if exists:
            print(f"  → '{tk}' already in group '{group_name}'. Skipping.\n")
            continue

        while True:
            try:
                fetched = fetch_from_yfinance(tk)
                print(f"  → Fetched data for {tk}:")
                print(f"      Name         : {fetched['Name']}")
                print(f"      Sector       : {fetched['Sector']}")
                print(f"      Industry     : {fetched['Industry']}")
                print(f"      Current Price: {fetched['Current Price']}")
                print(f"      Market Cap   : {fetched['Market Cap']}")
                print(f"      PE Ratio     : {fetched['PE Ratio']}")
                print(f"      Dividend Yld : {fetched['Dividend Yield']}")
                break
            except Exception as e:
                print(f"  × Fetching '{tk}' failed: {e}")
                corrected = confirm_or_adjust_ticker(tk)
                if not corrected:
                    print(f"  → Cancelling '{tk}'.\n")
                    fetched = None
                    break
                tk = corrected

        if fetched is None:
            continue

        override = input(
            "  Is this information correct? (Y to accept / N to fill manually): "
        ).strip().lower()
        if override in ("n", "no"):
            manual_data = prompt_manual_entry(tk)
            fetched = manual_data

        # Prepend group name to the row data
        row_data = {"Group": group_name}
        for k, v in fetched.items():
            row_data[k] = parse_number(v) if k in NUMERIC_FIELDS else v

        # Append via loc to avoid FutureWarning
        groups.loc[len(groups)] = row_data
        print(f"  ✓ Added '{tk}' to group '{group_name}'.\n")

    return groups


def remove_ticker_from_group(groups: pd.DataFrame) -> pd.DataFrame:
    """
    Prompt for group and ticker to remove.
    """
    if groups.empty:
        print("No groups defined yet.\n")
        return groups

    print("\nExisting groups:")
    unique_groups = groups["Group"].dropna().unique().tolist()
    for i, g in enumerate(unique_groups, start=1):
        print(f"  {i}) {g}")
    choice = input(
        f"Select a group to modify [1-{len(unique_groups)}] (or press Enter to cancel): "
    ).strip()
    if not choice:
        print("Canceled.\n")
        return groups
    if not (choice.isdigit() and 1 <= int(choice) <= len(unique_groups)):
        print_invalid_choice()
        return groups

    grp = unique_groups[int(choice) - 1]
    print(f"\nMembers of '{grp}':")
    members = groups[groups["Group"] == grp]["Ticker"].tolist()
    for i, t in enumerate(members, start=1):
        print(f"  {i}) {t}")
    idx = input(
        f"Select ticker to remove (1-{len(members)}) (or press Enter to cancel): "
    ).strip()
    if not idx:
        print("Canceled.\n")
        return groups
    if not (idx.isdigit() and 1 <= int(idx) <= len(members)):
        print_invalid_choice()
        return groups

    to_remove = members[int(idx) - 1]
    groups = groups[~((groups["Group"] == grp) & (groups["Ticker"] == to_remove))]
    groups = groups.reset_index(drop=True)
    print(f"  ✓ Removed '{to_remove}' from group '{grp}'.\n")
    return groups


def delete_group(groups: pd.DataFrame) -> pd.DataFrame:
    """
    Prompt for a group to delete entirely (all its tickers).
    """
    if groups.empty:
        print("No groups defined yet.\n")
        return groups

    print("\nExisting groups:")
    unique_groups = groups["Group"].dropna().unique().tolist()
    for i, g in enumerate(unique_groups, start=1):
        print(f"  {i}) {g}")
    choice = input(
        f"Select a group to delete [1-{len(unique_groups)}] (or press Enter to cancel): "
    ).strip()
    if not choice:
        print("Canceled.\n")
        return groups
    if not (choice.isdigit() and 1 <= int(choice) <= len(unique_groups)):
        print_invalid_choice()
        return groups

    grp = unique_groups[int(choice) - 1]
    groups = groups[groups["Group"] != grp].reset_index(drop=True)
    print(f"  ✓ Deleted entire group '{grp}'.\n")
    return groups


def view_groups(groups: pd.DataFrame):
    """
    Display all groups and their members in a readable format.
    """
    if groups.empty:
        print("No groups defined yet.\n")
        return

    print("\n=== All Groups & Members ===\n")
    for grp in groups["Group"].dropna().unique():
        print(f"Group: {grp}")
        sub = groups[groups["Group"] == grp][["Ticker", "Name", "Sector", "Industry", "Current Price"]]
        print_table(sub)
        summary = portfolio_summary(sub)
        if not summary.empty:
            print_table(summary, showindex=True)
        print("")


def main():
    print_header("\U0001F4CA Group Analysis Manager")
    portfolio = load_portfolio()
    groups = load_groups()

    while True:
        print("Choose an action:")
        options = [
            "View all groups",
            "Create a new group (or link to portfolio)",
            "Add ticker(s) to an existing group",
            "Remove ticker from a group",
            "Delete an entire group",
            "Exit",
        ]
        print_menu(options)
        choice = input(f"Select an option [1-{len(options)}]: ").strip()

        if choice == "1":
            view_groups(groups)

        elif choice == "2":
            grp_name = choose_group(portfolio)
            if not grp_name:
                print("No group name entered; canceling.\n")
            else:
                # If group already exists, notify; otherwise create empty placeholder row
                existing = groups["Group"].dropna().astype(str).values
                if grp_name in existing:
                    print(f"Group '{grp_name}' already exists. You can add members later.\n")
                else:
                    # Create an empty placeholder row so group shows up
                    placeholder = {col: pd.NA for col in COLUMNS}
                    placeholder["Group"] = grp_name
                    placeholder["Ticker"] = ""
                    groups.loc[len(groups)] = placeholder
                    print(f"  ✓ Created new group '{grp_name}'.\n")
                save_groups(groups)

        elif choice == "3":
            if groups.empty:
                print("No groups exist. Create one first.\n")
            else:
                print("\nExisting groups:")
                unique_groups = groups["Group"].dropna().unique().tolist()
                for i, g in enumerate(unique_groups, start=1):
                    print(f"  {i}) {g}")
                sel = input(
                    f"Select a group [1-{len(unique_groups)}] (or press Enter to cancel): "
                ).strip()
                if not sel:
                    print("Canceled.\n")
                elif sel.isdigit() and 1 <= int(sel) <= len(unique_groups):
                    grp_name = unique_groups[int(sel) - 1]
                    groups = add_tickers_to_group(groups, grp_name)
                    save_groups(groups)
                else:
                    print_invalid_choice()

        elif choice == "4":
            groups = remove_ticker_from_group(groups)
            save_groups(groups)

        elif choice == "5":
            groups = delete_group(groups)
            save_groups(groups)

        elif choice == "6":
            print("Exiting Group Analysis Manager.")
            break

        else:
            print_invalid_choice()


if __name__ == "__main__":
    main()
