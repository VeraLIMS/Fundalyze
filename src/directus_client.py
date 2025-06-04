import os
import requests
from typing import Any, Dict, List

# Environment variables may include a trailing slash; remove it for safety
DIRECTUS_URL = os.getenv("DIRECTUS_URL", "").rstrip("/")
DIRECTUS_TOKEN = os.getenv("DIRECTUS_TOKEN", "")

_session = requests.Session()
if DIRECTUS_TOKEN:
    _session.headers.update({"Authorization": f"Bearer {DIRECTUS_TOKEN}"})


def fetch_items(collection: str) -> List[Dict[str, Any]]:
    """Fetch all items from a Directus collection."""
    url = f"{DIRECTUS_URL}/items/{collection}"
    resp = _session.get(url, params={"limit": -1}, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, dict):
        return data.get("data", [])
    return data
