#!/usr/bin/env python3
"""Check connectivity to the Directus API configured in ``config/.env``.

The script loads environment variables via ``modules.config_utils.load_settings``
and then attempts a GET request to ``DIRECTUS_URL/server/health``.
It prints the HTTP status and a short snippet of the response so you can
inspect whether authentication or network issues are present.
"""

from __future__ import annotations

import os
import sys
import requests

SCRIPT_DIR = os.path.dirname(__file__)
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from modules.config_utils import load_settings


def main() -> None:
    load_settings()
    url = os.getenv("DIRECTUS_URL")
    if not url:
        print("DIRECTUS_URL not configured")
        sys.exit(1)

    endpoint = f"{url.rstrip('/')}/server/health"
    print(f"Connecting to {endpoint}…")
    try:
        resp = requests.get(endpoint, timeout=10)
    except requests.exceptions.RequestException as exc:
        print(f"Request failed: {exc}")
        sys.exit(1)

    print(f"HTTP {resp.status_code}")
    snippet = resp.text[:200].replace("\n", " ")
    print(f"Response: {snippet}")

    if not resp.ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
