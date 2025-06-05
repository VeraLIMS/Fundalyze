import json

from modules.interface import print_invalid_choice

from modules.data import directus_client as dc

try:
    from modules.management.settings_manager.wizards.directus_setup import (
        run_wizard as _directus_setup,
    )
except Exception:  # pragma: no cover - wizard optional
    _directus_setup = None


def run_directus_wizard() -> None:
    """Interactive wizard for common Directus API operations."""
    if not dc.DIRECTUS_URL:
        print("DIRECTUS_URL not configured in config/.env")
        if _directus_setup:
            _directus_setup()
            dc.reload_env()
        if not dc.DIRECTUS_URL:
            print()
            return

    while True:
        print("\n🧩 Directus Tools")
        print("1) List Collections")
        print("2) View Fields in Collection")
        print("3) Add Field to Collection")
        print("4) Fetch Items from Collection")
        print("5) Insert Item into Collection")
        print("6) Return to Main Menu")
        choice = input("Select an option [1-6]: ").strip()

        if choice == "1":
            cols = dc.list_collections()
            print("Available collections:")
            for c in cols:
                print(f"  - {c}")
        elif choice == "2":
            col = input("Collection name: ").strip()
            if col:
                fields = dc.list_fields(col)
                print(f"Fields for '{col}':")
                for f in fields:
                    print(f"  - {f}")
        elif choice == "3":
            col = input("Collection name: ").strip()
            field = input("New field name: ").strip()
            ftype = input("Field type [string]: ").strip() or "string"
            if col and field:
                dc.create_field(col, field, ftype)
                print("Field created.\n")
        elif choice == "4":
            col = input("Collection name: ").strip()
            if col:
                items = dc.fetch_items(col)
                print(json.dumps(items, indent=2))
        elif choice == "5":
            col = input("Collection name: ").strip()
            raw = input("JSON for single item: ").strip()
            if col and raw:
                try:
                    data = json.loads(raw)
                except Exception as exc:
                    print(f"Invalid JSON: {exc}\n")
                else:
                    dc.insert_items(col, [data])
                    print("Item inserted.\n")
        elif choice == "6":
            break
        else:
            print_invalid_choice()
