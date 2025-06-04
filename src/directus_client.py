import os
from typing import Any, Dict, List

import requests

# Environment variables may include a trailing slash; remove it for safety
DIRECTUS_URL = os.getenv("DIRECTUS_URL", "").rstrip("/")
DIRECTUS_TOKEN = os.getenv("DIRECTUS_TOKEN")

_session = requests.Session()
if DIRECTUS_TOKEN:
    _session.headers.update({"Authorization": f"Bearer {DIRECTUS_TOKEN}"})


def list_fields(collection: str) -> List[str]:
    """Return list of field names for the given Directus collection."""
    if not DIRECTUS_URL:
        raise RuntimeError("DIRECTUS_URL not configured")
    resp = _session.get(f"{DIRECTUS_URL}/fields/{collection}", timeout=10)
    resp.raise_for_status()
    data = resp.json().get("data", [])
    return [f.get("field") for f in data]


def fetch_items(collection: str) -> List[Dict[str, Any]]:
    """Fetch all items from a Directus collection."""
    if not DIRECTUS_URL:
        raise RuntimeError("DIRECTUS_URL not configured")
    resp = _session.get(
        f"{DIRECTUS_URL}/items/{collection}", params={"limit": -1}, timeout=10
    )
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, dict):
        return data.get("data", [])
    return data


def insert_items(collection: str, items):
    """Insert one or more items into a Directus collection."""
    if not DIRECTUS_URL:
        raise RuntimeError("DIRECTUS_URL not configured")
    payload = {"data": items}
    resp = _session.post(
        f"{DIRECTUS_URL}/items/{collection}", json=payload, timeout=10
    )
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, dict):
        return data.get("data")
    return data
