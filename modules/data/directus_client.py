import os
import requests

from modules.config_utils import load_settings  # noqa: E402

load_settings()  # ensure .env is read when this module is imported

DIRECTUS_URL = os.getenv("DIRECTUS_URL")
DIRECTUS_TOKEN = os.getenv("DIRECTUS_TOKEN")


def _headers():
    if DIRECTUS_TOKEN:
        return {"Authorization": f"Bearer {DIRECTUS_TOKEN}"}
    return {}


def list_fields(collection: str):
    """Return list of field names for the given Directus collection."""
    if not DIRECTUS_URL:
        raise RuntimeError("DIRECTUS_URL not configured")
    resp = requests.get(f"{DIRECTUS_URL}/fields/{collection}", headers=_headers())
    resp.raise_for_status()
    data = resp.json().get("data", [])
    return [f.get("field") for f in data]


def fetch_items(collection: str):
    """Fetch all items from a Directus collection."""
    if not DIRECTUS_URL:
        raise RuntimeError("DIRECTUS_URL not configured")
    resp = requests.get(f"{DIRECTUS_URL}/items/{collection}", headers=_headers())
    resp.raise_for_status()
    return resp.json().get("data", [])


def insert_items(collection: str, items):
    """Insert one or more items into a Directus collection."""
    if not DIRECTUS_URL:
        raise RuntimeError("DIRECTUS_URL not configured")
    payload = {"data": items}
    resp = requests.post(f"{DIRECTUS_URL}/items/{collection}", json=payload, headers=_headers())
    resp.raise_for_status()
    return resp.json().get("data")

