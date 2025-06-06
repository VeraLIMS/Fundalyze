#!/usr/bin/env python3
"""Field mapping diagnostic helper for Fundalyze."""
import argparse
from modules.management.portfolio_manager import portfolio_manager as pm
from modules.management.group_analysis import group_analysis as ga
from modules.data.directus_mapper import (
    load_field_map,
    prepare_records,
    add_missing_mappings,
)
from modules.data.directus_client import insert_items, fetch_items

COLLECTIONS = {
    pm.get_portfolio_collection(): pm.COLUMNS,
    ga.GROUPS_COLLECTION: ga.COLUMNS,
}

def show_mapping(collection: str, expected: list[str]) -> None:
    mapping = load_field_map().get("collections", {}).get(collection, {}).get("fields", {})
    print(f"\n[{collection}] expected keys -> mapped fields")
    for key in expected:
        entry = mapping.get(key)
        target = entry.get("mapped_to") if entry else None
        print(f"  {key} -> {target}")


def test_insert(ticker: str = "MSFT") -> None:
    from modules.management.portfolio_manager.portfolio_manager import (
        fetch_from_unified,
        get_portfolio_collection,
    )

    record = fetch_from_unified(ticker)
    if not record:
        print("Fetch failed")
        return
    print("Original:", record)
    collection = get_portfolio_collection()
    add_missing_mappings(collection, [record])
    prepared = prepare_records(collection, [record], verbose=True)[0]
    print("Prepared:", prepared)
    res = insert_items(collection, [prepared])
    print("Insert result:", res)
    if res:
        fetched = fetch_items(collection, limit=1)
        print("Fetched back:", fetched)


def main() -> None:
    parser = argparse.ArgumentParser(description="Field mapping diagnostics")
    parser.add_argument(
        "--insert",
        action="store_true",
        help="Test inserting a record after displaying mapping",
    )
    parser.add_argument(
        "--ticker",
        default="MSFT",
        help="Ticker symbol to use with --insert",
    )
    args = parser.parse_args()

    for col, expected in COLLECTIONS.items():
        show_mapping(col, expected)

    if args.insert:
        print(f"\nRunning test insert with ticker {args.ticker}...")
        test_insert(args.ticker)


if __name__ == "__main__":
    main()
