from __future__ import annotations

"""Thin wrapper around the Directus REST API."""

import logging
import os
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 30


class DirectusClient:
    """Simple Directus API client.

    Parameters
    ----------
    base_url:
        Directus base URL. Falls back to ``DIRECTUS_URL`` env var.
    token:
        API token. Falls back to ``DIRECTUS_API_TOKEN`` or ``DIRECTUS_TOKEN``.
    """

    def __init__(self, base_url: Optional[str] = None, token: Optional[str] = None) -> None:
        self.base_url = base_url or os.getenv("DIRECTUS_URL", "")
        self.token = token or os.getenv("DIRECTUS_API_TOKEN") or os.getenv("DIRECTUS_TOKEN")
        if not self.base_url:
            raise RuntimeError("DIRECTUS_URL not configured")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _headers(self) -> Dict[str, str]:
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _request(self, method: str, path: str, **kwargs) -> Dict[str, Any] | None:
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        try:
            logger.debug("Directus request %s %s", method, url)
            resp = requests.request(
                method,
                url,
                headers=self._headers(),
                timeout=DEFAULT_TIMEOUT,
                **kwargs,
            )
            resp.raise_for_status()
        except requests.RequestException as exc:
            logger.error("Directus request failed: %s", exc)
            return None
        try:
            return resp.json()
        except ValueError:
            logger.error("Invalid JSON response from %s: %s", url, resp.text)
            return None

    # ------------------------------------------------------------------
    # Schema helpers
    # ------------------------------------------------------------------
    def list_collections(self) -> list[str]:
        data = self._request("GET", "collections") or {}
        return [c.get("collection") for c in data.get("data", [])]

    def list_fields(self, collection: str) -> list[Dict[str, Any]]:
        data = self._request("GET", f"fields/{collection}") or {}
        return data.get("data", [])

    def create_field(self, collection: str, field: str, definition: Dict[str, Any]) -> Any:
        payload = {"field": field}
        payload.update(definition)
        return self._request("POST", f"fields/{collection}", json=payload)

    def update_field(self, collection: str, field: str, definition: Dict[str, Any]) -> Any:
        return self._request("PATCH", f"fields/{collection}/{field}", json=definition)

    def delete_field(self, collection: str, field: str) -> Any:
        return self._request("DELETE", f"fields/{collection}/{field}")
