"""Interactive wizard for basic Directus API operations."""

import json

from modules.interface import (
    print_invalid_choice,
    print_header,
    input_or_cancel,
    print_menu,
)

from modules.data import (
    directus_client as dc,
    prepare_records,
    refresh_field_map,
    add_missing_mappings,
    load_field_map,
)
from modules.management.portfolio_manager import portfolio_manager as pm
from modules.management.group_analysis import group_analysis as ga

try:
    from modules.management.settings_manager.wizards.directus_setup import (
        run_wizard as _directus_setup,
    )
except Exception:  # pragma: no cover - wizard optional
    _directus_setup = None


def run_directus_wizard() -> None:
    """Interactive wizard for common Directus API operations."""
    # Reload environment variables in case the user recently updated config/.env
    dc.reload_env()

    if not dc.DIRECTUS_URL:
        print("DIRECTUS_URL not configured in config/.env")
        if _directus_setup:
            _directus_setup()
            dc.reload_env()
        if not dc.DIRECTUS_URL:
            print()
            return

    # Keep mapping in sync but avoid slowing down menu interactions
    refresh_field_map()

    while True:
        print_header("\U0001F9E9 Directus Tools")
        options = [
            "List Collections",
            "View Fields in Collection",
            "Add Field to Collection",
            "Fetch Items from Collection",
            "Insert Item into Collection",
            "Test Field Mapping",
            "Test Insert (MSFT)",
            "Refresh Field Map",
            "Return to Main Menu",
        ]
        print_menu(options)
        choice = input(f"Select an option [1-{len(options)}]: ").strip()

        if choice == "1":
            cols = dc.list_collections()
            print("Available collections:")
            for c in cols:
                print(f"  - {c}")
        elif choice == "2":
            col = input_or_cancel("Collection name")
            if not col:
                print("Canceled.\n")
            else:
                fields = dc.list_fields(col)
                print(f"Fields for '{col}':")
                for f in fields:
                    print(f"  - {f}")
        elif choice == "3":
            col = input_or_cancel("Collection name")
            if not col:
                print("Canceled.\n")
            else:
                field = input_or_cancel("New field name")
                if not field:
                    print("Canceled.\n")
                else:
                    ftype = input("Field type [string]: ").strip() or "string"
                    dc.create_field(col, field, ftype)
                    print("Field created.\n")
        elif choice == "4":
            col = input_or_cancel("Collection name")
            if not col:
                print("Canceled.\n")
            else:
                items = dc.fetch_items(col)
                print(json.dumps(items, indent=2))
        elif choice == "5":
            col = input_or_cancel("Collection name")
            if not col:
                print("Canceled.\n")
            else:
                raw = input_or_cancel("JSON for single item")
                if not raw:
                    print("Canceled.\n")
                else:
                    try:
                        data = json.loads(raw)
                    except Exception as exc:
                        print(f"Invalid JSON: {exc}\n")
                    else:
                        records = prepare_records(col, [data])
                        dc.insert_items(col, records)
                        print("Item inserted.\n")
        elif choice == "6":
            for col, cols in (
                (pm.get_portfolio_collection(), pm.COLUMNS),
                (ga.GROUPS_COLLECTION, ga.COLUMNS),
            ):
                mapping = load_field_map().get("collections", {}).get(col, {}).get("fields", {})
                print(f"\nMapping for {col}:")
                for c in cols:
                    tgt = mapping.get(c, {}).get("mapped_to")
                    print(f"  {c} -> {tgt}")
        elif choice == "7":
            from modules.management.portfolio_manager.portfolio_manager import (
                fetch_from_unified,
                get_portfolio_collection,
            )

            record = fetch_from_unified("MSFT")
            collection = get_portfolio_collection()
            add_missing_mappings(collection, [record])
            prepared = prepare_records(collection, [record], verbose=True)[0]
            dc.insert_items(collection, [prepared])
            print("Insert attempted. Check logs for details.\n")
        elif choice == "8":
            refresh_field_map()
            print("Field map updated.\n")
        elif choice == "9":
            break
        else:
            print_invalid_choice()
