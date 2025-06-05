"""Small helper utilities for report generation."""

from __future__ import annotations

from datetime import datetime, timezone


def iso_timestamp_utc() -> str:
    """Return the current UTC timestamp in ISO 8601 format."""
    return (
        datetime.now(tz=timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )

