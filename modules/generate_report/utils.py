from __future__ import annotations

"""Utility helpers used across the :mod:`generate_report` package."""

import time
from typing import Dict


def iso_timestamp_utc() -> str:
    """Return the current UTC timestamp in ISO 8601 format."""
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def record_file_metadata(metadata: Dict, filename: str, source: str, source_url: str = "") -> None:
    """Update ``metadata`` dict with file information.

    Parameters
    ----------
    metadata:
        The metadata dictionary with a ``files`` key.
    filename:
        Name of the file being recorded.
    source:
        Human readable description of the data source.
    source_url:
        Optional URL where the data was retrieved from.
    """

    files = metadata.setdefault("files", {})
    files[filename] = {
        "source": source,
        "source_url": source_url,
        "fetched_at": iso_timestamp_utc(),
    }

