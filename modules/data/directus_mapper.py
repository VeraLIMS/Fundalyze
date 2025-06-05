import json
from pathlib import Path
from typing import Iterable, Dict, Any, List

from .directus_client import list_fields

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MAP_FILE = PROJECT_ROOT / "config" / "directus_field_map.json"


def load_field_map() -> Dict[str, Dict[str, str]]:
    """Return mapping dictionary loaded from ``config/directus_field_map.json``."""
    if MAP_FILE.is_file():
        with open(MAP_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_field_map(mapping: Dict[str, Dict[str, str]]) -> None:
    """Save mapping dictionary to ``config/directus_field_map.json``."""
    MAP_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MAP_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2)


def prepare_records(collection: str, records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Rename and filter record fields for Directus insertion."""
    mapping = load_field_map().get(collection, {})
    try:
        allowed = set(list_fields(collection))
    except Exception:
        allowed = set()

    prepared: List[Dict[str, Any]] = []
    for row in records:
        mapped = {}
        for key, value in row.items():
            new_key = mapping.get(key, key)
            if not allowed or new_key in allowed:
                mapped[new_key] = value
        prepared.append(mapped)
    return prepared
