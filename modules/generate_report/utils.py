from __future__ import annotations

import time


def iso_timestamp_utc() -> str:
    """Return current UTC timestamp in ISO 8601 format."""
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

