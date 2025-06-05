"""Utilities for mapping DataFrame fields to Directus collections."""

import json
import logging
from pathlib import Path
from typing import Iterable, Dict, Any, List, TYPE_CHECKING

from .directus_client import list_fields_with_types, list_collections, list_fields

if TYPE_CHECKING:  # pragma: no cover - for type hints only
    import pandas as pd

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MAP_FILE = PROJECT_ROOT / "config" / "directus_field_map.json"


def load_field_map() -> Dict[str, Any]:
    """Return mapping dictionary loaded from ``config/directus_field_map.json``."""
    if MAP_FILE.is_file():
        with open(MAP_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "collections" not in data:
            converted = {"collections": {}}
            for col, fields in data.items():
                converted["collections"][col] = {
                    "fields": {
                        name: {"type": None, "mapped_to": dest}
                        for name, dest in fields.items()
                    }
                }
            return converted
        return data
    return {"collections": {}}


def save_field_map(mapping: Dict[str, Any]) -> None:
    """Save mapping dictionary to ``config/directus_field_map.json``."""
    MAP_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MAP_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2)


def prepare_records(collection: str, records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Rename and filter record fields for Directus insertion."""
    field_map = (
        load_field_map().get("collections", {})
        .get(collection, {})
        .get("fields", {})
    )
    try:
        allowed = set(list_fields(collection))
    except Exception:
        allowed = set()

    prepared: List[Dict[str, Any]] = []
    for row in records:
        logger.debug("Original record: %s", row)
        mapped = {}
        for key, value in row.items():
            entry = field_map.get(key)
            new_key = entry.get("mapped_to") if entry else key
            if not allowed or new_key in allowed:
                mapped[new_key] = value
        logger.debug("Mapped record: %s", mapped)
        prepared.append(mapped)
    return prepared


def interactive_prepare_records(
    collection: str, records: Iterable[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Like :func:`prepare_records` but prompt for unmapped fields.

    Any newly mapped fields are saved back to ``directus_field_map.json``.
    """
    mapping = load_field_map()
    col_entry = mapping.setdefault("collections", {}).setdefault(collection, {"fields": {}})
    field_map = col_entry.setdefault("fields", {})

    try:
        allowed = set(list_fields(collection))
    except Exception:
        allowed = set()

    updated = False
    prepared: List[Dict[str, Any]] = []
    for row in records:
        mapped = {}
        for key, value in row.items():
            entry = field_map.get(key)
            new_key = entry.get("mapped_to") if entry else None
            if new_key is None:
                prompt = (
                    f"Map column '{key}' to a Directus field for collection '{collection}' "
                    "(leave blank to skip): "
                )
                choice = input(prompt).strip()
                if choice:
                    field_map[key] = {"type": None, "mapped_to": choice}
                    new_key = choice
                    updated = True
            if new_key and (not allowed or new_key in allowed):
                mapped[new_key] = value
        prepared.append(mapped)

    if updated:
        save_field_map(mapping)
    return prepared


def refresh_field_map() -> Dict[str, Any]:
    """Update mapping with fields from Directus collections."""
    mapping = load_field_map()
    collections_dict = mapping.setdefault("collections", {})
    try:
        collections = list_collections()
    except Exception:
        collections = []

    for col in collections:
        try:
            fields = list_fields_with_types(col)
        except Exception:
            continue
        col_entry = collections_dict.setdefault(col, {"fields": {}})
        fields_map = col_entry.setdefault("fields", {})
        for f in fields:
            fields_map.setdefault(
                f["field"],
                {"type": f.get("type"), "mapped_to": f.get("field")},
            )

    save_field_map(mapping)
    return mapping


def ensure_field_mapping(collection: str, df: "pd.DataFrame") -> Dict[str, Any]:
    """Interactive mapping helper for DataFrame columns.

    For each column in ``df`` that is unmapped or mapped to a non-existent
    Directus field, prompt the user for the target field name. The mapping file
    is updated and returned.
    """

    import pandas as pd  # local import to avoid heavy dependency at startup

    if not isinstance(df, pd.DataFrame):  # pragma: no cover - defensive
        raise TypeError("df must be a pandas DataFrame")

    mapping = load_field_map()
    collections = mapping.setdefault("collections", {})
    col_entry = collections.setdefault(collection, {"fields": {}})
    fields_map = col_entry.setdefault("fields", {})

    try:
        allowed = list_fields(collection)
    except Exception:  # pragma: no cover - network/Directus unavailable
        allowed = []

    changed = False
    for column in df.columns:
        entry = fields_map.get(column)
        target = entry.get("mapped_to") if entry else None
        if not target or (allowed and target not in allowed):
            if allowed:
                print(f"Available Directus fields for '{collection}': {', '.join(allowed)}")
            prompt = f"Map column '{column}' to Directus field: "
            new_target = input(prompt).strip()
            if new_target:
                fields_map[column] = {"type": entry.get("type") if entry else None, "mapped_to": new_target}
                changed = True

    if changed:
        save_field_map(mapping)

    return mapping
