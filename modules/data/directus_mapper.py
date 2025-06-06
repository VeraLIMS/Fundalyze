"""Helpers for mapping local data fields to Directus collection fields."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Set

from .directus_client import list_collections, list_fields, list_fields_with_types

if TYPE_CHECKING:  # pragma: no cover - for type hints only
    import pandas as pd

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MAP_FILE = PROJECT_ROOT / "config" / "directus_field_map.json"
EXAMPLE_MAP_FILE = PROJECT_ROOT / "directus_field_map_example.json"


def load_field_map() -> Dict[str, Any]:
    """Return field mapping from ``config/directus_field_map.json``.

    If the file does not exist, fall back to ``directus_field_map_example.json``
    shipped with the repository. This helps new contributors run the project
    without first generating a custom mapping file.
    """
    if MAP_FILE.is_file():
        path = MAP_FILE
    elif MAP_FILE == PROJECT_ROOT / "config" / "directus_field_map.json" and EXAMPLE_MAP_FILE.is_file():
        path = EXAMPLE_MAP_FILE
    else:
        return {"collections": {}}

    data = json.loads(path.read_text(encoding="utf-8"))
    if "collections" not in data:
        data = _convert_legacy_format(data)
    return data


def _convert_legacy_format(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert legacy ``collection -> field`` mapping to the new schema."""
    converted: Dict[str, Any] = {"collections": {}}
    for col, fields in data.items():
        converted["collections"][col] = {
            "fields": {
                name: {"type": None, "mapped_to": dest}
                for name, dest in fields.items()
            }
        }
    return converted


def save_field_map(mapping: Dict[str, Any]) -> None:
    """Persist mapping dictionary to ``config/directus_field_map.json``."""
    MAP_FILE.parent.mkdir(parents=True, exist_ok=True)
    MAP_FILE.write_text(json.dumps(mapping, indent=2), encoding="utf-8")


def _get_allowed_fields(collection: str) -> Set[str]:
    """Return available Directus fields for ``collection``.

    Returns:
        Set of field names. Empty set if retrieval fails.
    """
    try:
        return set(list_fields(collection))
    except Exception:  # pragma: no cover - network/Directus unavailable
        return set()


def _map_row(
    row: Dict[str, Any],
    field_map: Dict[str, Any],
    allowed: Set[str],
    *,
    collection: str | None = None,
) -> Dict[str, Any]:
    """Return ``row`` with keys renamed according to ``field_map``.

    Args:
        row: Record to map.
        field_map: Mapping configuration for the collection.
        allowed: Allowed Directus field names. Empty to allow all.

    Returns:
        Mapped record ready for Directus insertion.
    """
    mapped: Dict[str, Any] = {}
    dropped: list[str] = []
    for key, value in row.items():
        entry = field_map.get(key)
        new_key = entry.get("mapped_to") if entry else key
        if not allowed or new_key in allowed:
            mapped[new_key] = value
        else:
            dropped.append(key)
    if dropped and collection:
        logger.warning(
            "Dropped keys for %s: %s", collection, ", ".join(dropped)
        )
        logger.debug("Current mapping for %s: %s", collection, field_map)
    logger.debug("Mapped record: %s", mapped)
    if row and not mapped:
        logger.error(
            "Mapping produced empty record. original=%s map=%s", row, field_map
        )
        logger.error("Dropped keys: %s", ", ".join(dropped))
        raise ValueError(
            "Mapped record is empty. Check field mapping configuration"
        )
    return mapped


def prepare_records(
    collection: str,
    records: Iterable[Dict[str, Any]],
    *,
    verbose: bool = False,
) -> List[Dict[str, Any]]:
    """Rename and filter record fields for Directus insertion.

    Args:
        collection: Target Directus collection.
        records: Iterable of raw record dictionaries.

    Returns:
        List of records with mapped field names.
    """
    field_map = (
        load_field_map().get("collections", {})
        .get(collection, {})
        .get("fields", {})
    )
    allowed = _get_allowed_fields(collection)

    prepared: List[Dict[str, Any]] = []
    for row in records:
        if verbose:
            logger.info("Original record: %s", row)
        mapped = _map_row(row, field_map, allowed, collection=collection)
        if verbose:
            logger.info("Mapped record: %s", mapped)
        prepared.append(mapped)
    return prepared


def interactive_prepare_records(
    collection: str, records: Iterable[Dict[str, Any]], *, verbose: bool = False
) -> List[Dict[str, Any]]:
    """Interactive version of :func:`prepare_records`.

    Unmapped fields trigger a user prompt to specify the target Directus
    field. New mappings are persisted to ``directus_field_map.json``.

    Args:
        collection: Target Directus collection.
        records: Iterable of raw record dictionaries.

    Returns:
        List of records with mapped field names.
    """
    mapping = load_field_map()
    col_entry = mapping.setdefault("collections", {}).setdefault(collection, {"fields": {}})
    field_map = col_entry.setdefault("fields", {})

    allowed = _get_allowed_fields(collection)

    updated = False
    prepared: List[Dict[str, Any]] = []
    for row in records:
        if verbose:
            logger.info("Original record: %s", row)
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
        if verbose:
            logger.info("Mapped record: %s", mapped)
        prepared.append(mapped)

    if updated:
        save_field_map(mapping)
    return prepared


def refresh_field_map() -> Dict[str, Any]:
    """Update mapping with fields from Directus collections.

    Returns:
        Updated mapping dictionary.
    """
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
    """Interactively ensure DataFrame columns are mapped to Directus fields.

    Args:
        collection: Target Directus collection.
        df: Source DataFrame.

    Returns:
        Updated mapping dictionary.
    """

    import pandas as pd  # local import to avoid heavy dependency at startup

    if not isinstance(df, pd.DataFrame):  # pragma: no cover - defensive
        raise TypeError("df must be a pandas DataFrame")

    mapping = load_field_map()
    collections = mapping.setdefault("collections", {})
    col_entry = collections.setdefault(collection, {"fields": {}})
    fields_map = col_entry.setdefault("fields", {})

    allowed = list(_get_allowed_fields(collection))

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


def add_missing_mappings(collection: str, records: Iterable[Dict[str, Any]]) -> None:
    """Ensure all keys in ``records`` exist in ``directus_field_map.json``."""
    mapping = load_field_map()
    col_entry = mapping.setdefault("collections", {}).setdefault(collection, {"fields": {}})
    fields_map = col_entry.setdefault("fields", {})
    updated = False
    for row in records:
        for key in row.keys():
            if key not in fields_map:
                fields_map[key] = {"type": None, "mapped_to": key}
                updated = True
    if updated:
        save_field_map(mapping)
