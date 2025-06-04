import json

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
        print("\n=== Directus API Wizard ===")
        print("1) List collections")
        print("2) View fields of a collection")
        print("3) Add field to a collection")
        print("4) Fetch items from a collection")
        print("5) Insert item into a collection")
        print("6) Exit")
        choice = input("Select 1-6: ").strip()

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
            print("Invalid choice.\n")
