#!/usr/bin/env python3
"""Field mapping diagnostic helper for Fundalyze."""
from modules.management.portfolio_manager import portfolio_manager as pm
from modules.management.group_analysis import group_analysis as ga
from modules.data.directus_mapper import load_field_map, prepare_records, add_missing_mappings
from modules.data.directus_client import insert_items, fetch_items

COLLECTIONS = {
    pm.C_DIRECTUS_COLLECTION: pm.COLUMNS,
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
    from modules.management.portfolio_manager.portfolio_manager import fetch_from_unified, C_DIRECTUS_COLLECTION

    record = fetch_from_unified(ticker)
    if not record:
        print("Fetch failed")
        return
    print("Original:", record)
    add_missing_mappings(C_DIRECTUS_COLLECTION, [record])
    prepared = prepare_records(C_DIRECTUS_COLLECTION, [record], verbose=True)[0]
    print("Prepared:", prepared)
    res = insert_items(C_DIRECTUS_COLLECTION, [prepared])
    print("Insert result:", res)
    if res:
        fetched = fetch_items(C_DIRECTUS_COLLECTION, limit=1)
        print("Fetched back:", fetched)


if __name__ == "__main__":
    for col, expected in COLLECTIONS.items():
        show_mapping(col, expected)
    print("\nRunning test insert with ticker MSFT...")
    test_insert()
