#!/usr/bin/env python3
"""Synchronize Directus field mappings with an interactive CLI."""
from __future__ import annotations

from typing import Any, Dict, List

from modules.data.directus_client import (
    list_collections,
    list_fields_with_types,
)
from modules.data.directus_mapper import load_field_map, save_field_map, MAP_FILE  # noqa: F401


def prompt_user(question: str, options: List[str]) -> str:
    opts = [o.lower() for o in options]
    while True:
        resp = input(question).strip().lower()
        if resp in opts:
            return resp
        print(f"Enter one of: {', '.join(options)}")


def summarize_changes(changes: Dict[str, Any]) -> None:
    print("\nSummary of changes:")
    if changes.get("collections_added"):
        print("  Collections added:", ", ".join(changes["collections_added"]))
    if changes.get("collections_removed"):
        print("  Collections removed:", ", ".join(changes["collections_removed"]))
    if changes.get("fields_added"):
        for col, flds in changes["fields_added"].items():
            print(f"  Fields added to {col}: {', '.join(flds)}")
    if changes.get("fields_removed"):
        for col, flds in changes["fields_removed"].items():
            print(f"  Fields removed from {col}: {', '.join(flds)}")
    if changes.get("types_updated"):
        print("  Types updated:", ", ".join(changes["types_updated"]))


def main() -> None:
    mapping = load_field_map()
    collections_map = mapping.setdefault("collections", {})
    changes: Dict[str, Any] = {
        "collections_added": [],
        "collections_removed": [],
        "fields_added": {},
        "fields_removed": {},
        "types_updated": [],
    }

    try:
        directus_cols = list_collections()
    except Exception as exc:  # pragma: no cover - network
        print(f"Failed to fetch collections: {exc}")
        return

    existing_cols = set(collections_map.keys())
    for col in directus_cols:
        if col not in existing_cols:
            print(f'New collection detected: "{col}"')
            collections_map[col] = {"fields": {}}
            changes["collections_added"].append(col)

    for col in existing_cols - set(directus_cols):
        choice = prompt_user(
            f'Collection "{col}" no longer exists. Remove from JSON? [yes/no]: ',
            ["yes", "no"],
        )
        if choice == "yes":
            del collections_map[col]
            changes["collections_removed"].append(col)

    for col in directus_cols:
        try:
            fields = list_fields_with_types(col)
        except Exception as exc:  # pragma: no cover - network
            print(f"Failed to fetch fields for '{col}': {exc}")
            continue
        col_entry = collections_map.setdefault(col, {"fields": {}})
        fields_map = col_entry.setdefault("fields", {})

        existing_fields = set(fields_map.keys())
        directus_fields = {f["field"]: f.get("type") for f in fields}

        for fname, ftype in directus_fields.items():
            if fname not in existing_fields:
                print(
                    f'\n[NEW FIELD] Collection "{col}", field "{fname}" (type: "{ftype}")'
                )
                target = input(
                    "Enter target name (or press Enter to keep same): "
                ).strip() or fname
                fields_map[fname] = {"type": ftype, "mapped_to": target}
                changes.setdefault("fields_added", {}).setdefault(col, []).append(fname)
            else:
                current_type = fields_map[fname].get("type")
                if current_type != ftype:
                    choice = prompt_user(
                        f'\n[TYPE CHANGE] "{fname}" in "{col}" was "{current_type}", now "{ftype}". Update type in JSON? [yes/no]: ',
                        ["yes", "no"],
                    )
                    if choice == "yes":
                        fields_map[fname]["type"] = ftype
                        changes.setdefault("types_updated", []).append(f"{col}.{fname}")

        for fname in existing_fields - set(directus_fields.keys()):
            choice = prompt_user(
                f'\n[DELETED FIELD] "{fname}" in "{col}" no longer exists in Directus. Remove from JSON? [yes/no]: ',
                ["yes", "no"],
            )
            if choice == "yes":
                del fields_map[fname]
                changes.setdefault("fields_removed", {}).setdefault(col, []).append(fname)

    summarize_changes(changes)
    if prompt_user("\nProceed to write changes to directus_field_map.json? [yes/no]: ", ["yes", "no"]) == "yes":
        save_field_map(mapping)
        print("directus_field_map.json updated successfully.")
    else:
        print("Aborted; no changes saved.")


if __name__ == "__main__":
    main()
