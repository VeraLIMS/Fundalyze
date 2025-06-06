from __future__ import annotations

"""Export and fetch schema definitions from Directus."""

import csv
import logging
from pathlib import Path
from typing import Any, Dict

from modules.api.directus_client import DirectusClient

logger = logging.getLogger(__name__)

CSV_COLUMNS = [
    "table_name",
    "field_name",
    "type",
    "precision",
    "scale",
    "required",
    "default",
]


def fetch_schema(client: DirectusClient) -> Dict[str, Dict[str, Dict[str, Any]]]:
    """Return schema information from Directus as nested dictionaries."""
    schema: Dict[str, Dict[str, Dict[str, Any]]] = {}
    for collection in client.list_collections():
        fields = client.list_fields(collection)
        for f in fields:
            schema.setdefault(collection, {})[f.get("field")] = f
    return schema


def export_schema(client: DirectusClient, output: str | Path) -> None:
    """Write current Directus schema to ``output`` CSV file."""
    csv_path = Path(output)
    rows = []
    for collection in client.list_collections():
        fields = client.list_fields(collection)
        for f in fields:
            rows.append(
                {
                    "table_name": collection,
                    "field_name": f.get("field"),
                    "type": f.get("type"),
                    "precision": f.get("precision"),
                    "scale": f.get("scale"),
                    "required": not (f.get("schema") or {}).get("is_nullable", True),
                    "default": f.get("default_value"),
                }
            )
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    logger.info("Schema definitions exported to %s", csv_path)
