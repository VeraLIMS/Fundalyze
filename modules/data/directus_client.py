"""Lightweight Directus REST client used across the project.

This module provides minimal wrappers around the Directus REST API so other
modules can interact with Directus without carrying additional dependencies or
boilerplate. Functions in this file are intentionally thin and return parsed
JSON dictionaries to keep them simple to test.
"""

from __future__ import annotations

import logging
import math
import os
from typing import Any, Dict, List, Iterable

import requests

from modules.config_utils import load_settings  # noqa: E402

load_settings()  # ensure .env is read when this module is imported

# Default to empty string so missing configuration doesn't silently point to
# localhost. Consumers should explicitly set DIRECTUS_URL or handle the error.
DIRECTUS_URL = os.getenv("DIRECTUS_URL", "")
# Support legacy DIRECTUS_TOKEN as well as DIRECTUS_API_TOKEN
DIRECTUS_TOKEN = os.getenv("DIRECTUS_API_TOKEN") or os.getenv("DIRECTUS_TOKEN")
# Support both underscore and hyphen env var names for Cloudflare credentials
CF_ACCESS_CLIENT_ID = os.getenv("CF_ACCESS_CLIENT_ID") or os.getenv(
    "CF-Access-Client-Id"
)
CF_ACCESS_CLIENT_SECRET = os.getenv("CF_ACCESS_CLIENT_SECRET") or os.getenv(
    "CF-Access-Client-Secret"
)

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 30  # seconds


def _build_url(path: str) -> str:
    """Return full API URL for the given path."""
    return f"{DIRECTUS_URL.rstrip('/')}/{path.lstrip('/')}"


def _log_request(method: str, url: str, payload: Any) -> None:
    """Log an outgoing request with optional payload."""
    if payload:
        logger.debug("Directus request %s %s payload=%s", method, url, payload)
    else:
        logger.debug("Directus request %s %s", method, url)


def _make_request(method: str, url: str, **kwargs) -> Dict[str, Any] | None:
    """Return parsed JSON from a HTTP request or ``None`` on error."""
    payload = kwargs.get("json") or kwargs.get("data") or kwargs.get("params")
    _log_request(method, url, payload)

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        **_headers(),
    }

    try:
        resp = requests.request(
            method,
            url,
            headers=headers,
            timeout=DEFAULT_TIMEOUT,
            **kwargs,
        )
        resp.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        status = getattr(resp, "status_code", "?")
        body = getattr(resp, "text", "")
        logger.error(
            "HTTP error: %s | URL: %s | Status: %s | Content: %s",
            http_err,
            url,
            status,
            body,
        )
        return None
    except requests.exceptions.RequestException as err:
        logger.error("Request error: %s | URL: %s", err, url)
        return None

    return _parse_response(resp, url)


def _parse_response(resp: requests.Response, url: str) -> Dict[str, Any] | None:
    """Return parsed JSON from ``resp`` or ``None`` on error."""
    if "text/html" in resp.headers.get("content-type", ""):
        logger.error(
            "Directus responded with HTML content. This usually indicates a login page or Cloudflare Access protection. URL: %s | Content: %.100s",
            url,
            resp.text,
        )
        return None
    try:
        return resp.json()
    except ValueError as exc:
        logger.error(
            "Invalid JSON response: %s | URL: %s | Content: %.100s",
            exc,
            url,
            resp.text,
        )
    return None


def clean_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """Return a sanitized copy of ``record``.

    Numeric ``NaN`` or infinite values are replaced with ``None`` to avoid
    serialization issues.

    Args:
        record: Original record dictionary.

    Returns:
        A copy of ``record`` with problematic floats replaced by ``None``.
    """
    cleaned = {}
    for key, value in record.items():
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            cleaned[key] = None
        else:
            cleaned[key] = value
    return cleaned


def reload_env() -> None:
    """Reload environment variables used for Directus communication."""
    load_settings()  # ensures .env is loaded
    global DIRECTUS_URL, DIRECTUS_TOKEN, CF_ACCESS_CLIENT_ID, CF_ACCESS_CLIENT_SECRET
    # Do not fall back to localhost automatically when reloading
    DIRECTUS_URL = os.getenv("DIRECTUS_URL", "")
    DIRECTUS_TOKEN = os.getenv("DIRECTUS_API_TOKEN") or os.getenv("DIRECTUS_TOKEN")
    CF_ACCESS_CLIENT_ID = os.getenv("CF_ACCESS_CLIENT_ID") or os.getenv(
        "CF-Access-Client-Id"
    )
    CF_ACCESS_CLIENT_SECRET = os.getenv("CF_ACCESS_CLIENT_SECRET") or os.getenv(
        "CF-Access-Client-Secret"
    )


def _headers() -> Dict[str, str]:
    """Return authentication headers for Directus requests."""
    headers: Dict[str, str] = {}
    if DIRECTUS_TOKEN:
        headers["Authorization"] = f"Bearer {DIRECTUS_TOKEN}"
    if CF_ACCESS_CLIENT_ID:
        headers["CF-Access-Client-Id"] = CF_ACCESS_CLIENT_ID
    if CF_ACCESS_CLIENT_SECRET:
        headers["CF-Access-Client-Secret"] = CF_ACCESS_CLIENT_SECRET
    return headers


def _extract_data(result: Dict[str, Any] | None) -> List[Any]:
    """Return ``result['data']`` if present else an empty list."""
    return result.get("data", []) if result else []


def directus_request(method: str, path: str, **kwargs) -> Dict[str, Any] | None:
    """Send a request to the Directus API.

    Args:
        method: HTTP verb such as ``"GET"`` or ``"POST"``.
        path: API path relative to the Directus base URL.
        **kwargs: Additional options forwarded to ``requests.request``.

    Returns:
        Parsed JSON from the response or ``None`` if an error occurred.
    """
    if not DIRECTUS_URL:
        raise RuntimeError("DIRECTUS_URL not configured")

    url = _build_url(path)
    return _make_request(method, url, **kwargs)

def list_collections() -> list[str]:
    """Return available collection names."""
    result = directus_request("GET", "collections")
    return [c.get("collection") for c in _extract_data(result)]


def list_fields(collection: str) -> list[str]:
    """Return list of field names for the given Directus collection."""
    result = directus_request("GET", f"fields/{collection}")
    return [f.get("field") for f in _extract_data(result)]


def list_fields_with_types(collection: str) -> list[Dict[str, Any]]:
    """Return field metadata including name and type for a collection."""
    result = directus_request("GET", f"fields/{collection}")
    return [
        {"field": f.get("field"), "type": f.get("type")}
        for f in _extract_data(result)
    ]


def fetch_items(collection: str, limit: int | None = None) -> list[Dict[str, Any]]:
    """Fetch items from a Directus collection."""
    endpoint = f"items/{collection}"
    if limit is not None:
        endpoint += f"?limit={limit}"
    result = directus_request("GET", endpoint)
    return _extract_data(result)


def fetch_items_filtered(collection: str, params: Dict[str, Any]) -> list[Dict[str, Any]]:
    """Fetch items from ``collection`` applying Directus filter parameters."""
    payload = {"filter": params}
    result = directus_request("GET", f"items/{collection}", params=payload)
    return _extract_data(result)


def insert_items(collection: str, items):
    """Insert one or more items into a Directus collection.

    Any numeric NaN/inf values are converted to ``None`` before submission.
    """
    if not items:
        logger.warning("No records to insert.")
        return []

    cleaned = []
    for item in items:
        if isinstance(item, dict):
            cleaned.append(clean_record(item))
        else:
            cleaned.append(item)

    fields = cleaned[0].keys() if isinstance(cleaned[0], dict) else None
    create_collection_if_missing(collection, fields)

    payload = {"data": cleaned}
    logger.info("Inserting into %s: %s", collection, payload)
    result = directus_request("POST", f"items/{collection}", json=payload)
    data = _extract_data(result)
    if not data:
        logger.warning(
            "Insertion returned no data for %s | status/content: %s",
            collection,
            result,
        )
    return data


def create_field(collection: str, field: str, field_type: str = "string", **kwargs):
    """Create a new field in the given collection."""
    payload = {"field": field, "type": field_type}
    payload.update(kwargs)
    result = directus_request("POST", f"fields/{collection}", json=payload)
    data = _extract_data(result)
    return data if data else None


def create_collection_if_missing(collection: str, fields: Iterable[str] | None = None) -> bool:
    """Create ``collection`` and optional ``fields`` if it doesn't exist."""
    try:
        existing = list_collections()
    except Exception:
        return False
    if collection in existing:
        return False

    payload = {"collection": collection}
    res = directus_request("POST", "collections", json=payload)
    if res is None:
        logger.error("Failed to create collection %s", collection)
        return False

    if fields:
        for f in fields:
            try:
                create_field(collection, str(f))
            except Exception:
                logger.warning("Could not create field %s in %s", f, collection)
    return True


def update_item(collection: str, item_id: Any, updates: Dict[str, Any]):
    """Update a single item by ``item_id`` in ``collection``."""
    updates = clean_record(updates)
    result = directus_request("PATCH", f"items/{collection}/{item_id}", json=updates)
    data = _extract_data(result)
    return data if data else None


def delete_item(collection: str, item_id: Any) -> bool:
    """Delete an item by ``item_id`` from ``collection``."""
    result = directus_request("DELETE", f"items/{collection}/{item_id}")
    return result is not None

