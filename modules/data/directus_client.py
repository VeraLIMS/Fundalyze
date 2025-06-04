import os
import requests
from typing import Any, Dict

from modules.config_utils import load_settings  # noqa: E402

load_settings()  # ensure .env is read when this module is imported

DIRECTUS_URL = os.getenv("DIRECTUS_URL")
DIRECTUS_TOKEN = os.getenv("DIRECTUS_TOKEN")


def _headers():
    if DIRECTUS_TOKEN:
        return {"Authorization": f"Bearer {DIRECTUS_TOKEN}"}
    return {}


def directus_request(method: str, path: str, **kwargs) -> Dict[str, Any]:
    """Helper to send an authenticated request to the Directus API."""
    if not DIRECTUS_URL:
        raise RuntimeError("DIRECTUS_URL not configured")
    url = f"{DIRECTUS_URL.rstrip('/')}/{path.lstrip('/')}"
    resp = requests.request(method, url, headers=_headers(), **kwargs)
    resp.raise_for_status()
    return resp.json()

def list_collections() -> list[str]:
    """Return available collection names."""
    data = directus_request("GET", "collections").get("data", [])
    return [c.get("collection") for c in data]


def list_fields(collection: str) -> list[str]:
    """Return list of field names for the given Directus collection."""
    data = directus_request("GET", f"fields/{collection}").get("data", [])
    return [f.get("field") for f in data]


def fetch_items(collection: str):
    """Fetch all items from a Directus collection."""
    data = directus_request("GET", f"items/{collection}").get("data", [])
    return data


def insert_items(collection: str, items):
    """Insert one or more items into a Directus collection."""
    payload = {"data": items}
    data = directus_request("POST", f"items/{collection}", json=payload).get("data")
    return data


def create_field(collection: str, field: str, field_type: str = "string", **kwargs):
    """Create a new field in the given collection."""
    payload = {"field": field, "type": field_type}
    payload.update(kwargs)
    data = directus_request("POST", f"fields/{collection}", json=payload).get("data")
    return data

