"""Minimal Directus REST client used throughout Fundalyze.

The module lazily reads credentials from ``config/.env`` and exposes helper
functions for common CRUD operations. When Directus is not configured the
wrappers simply return ``None`` so the rest of the code can continue to operate
in a local-only mode.
"""

import os
import logging
import math
import requests
from typing import Any, Dict

from modules.config_utils import load_settings  # noqa: E402

load_settings()  # ensure .env is read when this module is imported

DIRECTUS_URL = os.getenv("DIRECTUS_URL", "http://localhost:8055")
# Support legacy DIRECTUS_TOKEN as well as DIRECTUS_API_TOKEN
DIRECTUS_TOKEN = os.getenv("DIRECTUS_API_TOKEN") or os.getenv("DIRECTUS_TOKEN")
CF_ACCESS_CLIENT_ID = os.getenv("CF_ACCESS_CLIENT_ID")
CF_ACCESS_CLIENT_SECRET = os.getenv("CF_ACCESS_CLIENT_SECRET")

logger = logging.getLogger(__name__)


def clean_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """Return a copy of ``record`` with NaN/inf values converted to ``None``."""
    cleaned = {}
    for key, value in record.items():
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            cleaned[key] = None
        else:
            cleaned[key] = value
    return cleaned


def reload_env() -> None:
    """Reload Directus environment variables from ``config/.env``."""
    load_settings()  # ensures .env is loaded
    global DIRECTUS_URL, DIRECTUS_TOKEN, CF_ACCESS_CLIENT_ID, CF_ACCESS_CLIENT_SECRET
    DIRECTUS_URL = os.getenv("DIRECTUS_URL", "http://localhost:8055")
    DIRECTUS_TOKEN = os.getenv("DIRECTUS_API_TOKEN") or os.getenv("DIRECTUS_TOKEN")
    CF_ACCESS_CLIENT_ID = os.getenv("CF_ACCESS_CLIENT_ID")
    CF_ACCESS_CLIENT_SECRET = os.getenv("CF_ACCESS_CLIENT_SECRET")


def _headers():
    """Return authentication headers for Directus requests."""
    headers = {}
    if DIRECTUS_TOKEN:
        headers["Authorization"] = f"Bearer {DIRECTUS_TOKEN}"
    if CF_ACCESS_CLIENT_ID:
        headers["CF-Access-Client-Id"] = CF_ACCESS_CLIENT_ID
    if CF_ACCESS_CLIENT_SECRET:
        headers["CF-Access-Client-Secret"] = CF_ACCESS_CLIENT_SECRET
    return headers


def directus_request(method: str, path: str, **kwargs) -> Dict[str, Any] | None:
    """Send a request to the Directus API and return the JSON response."""
    if not DIRECTUS_URL:
        raise RuntimeError("DIRECTUS_URL not configured")

    url = f"{DIRECTUS_URL.rstrip('/')}/{path.lstrip('/')}"
    payload = kwargs.get("json") or kwargs.get("data") or kwargs.get("params")
    if payload:
        logger.debug("Directus request %s %s payload=%s", method, url, payload)
    else:
        logger.debug("Directus request %s %s", method, url)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    headers.update(_headers())
    try:
        resp = requests.request(method, url, headers=headers, timeout=30, **kwargs)
        resp.raise_for_status()
        try:
            return resp.json()
        except ValueError as exc:
            # HTML login pages or other non-JSON content will trigger this
            logger.error(
                "Invalid JSON response: %s | URL: %s | Content: %.100s",
                exc,
                url,
                resp.text,
            )
            return None
    except requests.exceptions.HTTPError as errh:
        status = getattr(resp, "status_code", "?")
        body = getattr(resp, "text", "")
        logger.error(
            "HTTP error: %s | URL: %s | Status: %s | Content: %s",
            errh,
            url,
            status,
            body,
        )
    except requests.exceptions.RequestException as err:
        logger.error("Request error: %s | URL: %s", err, url)
    return None

def list_collections() -> list[str]:
    """Return available collection names."""
    result = directus_request("GET", "collections")
    data = result.get("data", []) if result else []
    return [c.get("collection") for c in data]


def list_fields(collection: str) -> list[str]:
    """Return list of field names for the given Directus collection."""
    result = directus_request("GET", f"fields/{collection}")
    data = result.get("data", []) if result else []
    return [f.get("field") for f in data]


def list_fields_with_types(collection: str) -> list[Dict[str, Any]]:
    """Return field metadata including name and type for a collection."""
    result = directus_request("GET", f"fields/{collection}")
    data = result.get("data", []) if result else []
    fields = []
    for f in data:
        fields.append({"field": f.get("field"), "type": f.get("type")})
    return fields


def fetch_items(collection: str, limit: int | None = None) -> list[Dict[str, Any]]:
    """Fetch items from a Directus collection."""
    endpoint = f"items/{collection}"
    if limit is not None:
        endpoint += f"?limit={limit}"
    result = directus_request("GET", endpoint)
    return result.get("data", []) if result else []


def fetch_items_filtered(collection: str, params: Dict[str, Any]) -> list[Dict[str, Any]]:
    """Fetch items from ``collection`` applying Directus filter parameters."""
    payload = {"filter": params}
    result = directus_request("GET", f"items/{collection}", params=payload)
    return result.get("data", []) if result else []


def insert_items(collection: str, items):
    """Insert one or more items into a Directus collection."""
    if not items:
        logger.warning("No records to insert.")
        return []

    cleaned = []
    for item in items:
        if isinstance(item, dict):
            cleaned.append(clean_record(item))
        else:
            cleaned.append(item)

    payload = {"data": cleaned}
    result = directus_request("POST", f"items/{collection}", json=payload)
    return result.get("data") if result else []


def create_field(collection: str, field: str, field_type: str = "string", **kwargs):
    """Create a new field in the given collection."""
    payload = {"field": field, "type": field_type}
    payload.update(kwargs)
    result = directus_request("POST", f"fields/{collection}", json=payload)
    return result.get("data") if result else None


def update_item(collection: str, item_id: Any, updates: Dict[str, Any]):
    """Update a single item by ``item_id`` in ``collection``."""
    updates = clean_record(updates)
    result = directus_request("PATCH", f"items/{collection}/{item_id}", json=updates)
    return result.get("data") if result else None


def delete_item(collection: str, item_id: Any) -> bool:
    """Delete an item by ``item_id`` from ``collection``."""
    result = directus_request("DELETE", f"items/{collection}/{item_id}")
    return result is not None

