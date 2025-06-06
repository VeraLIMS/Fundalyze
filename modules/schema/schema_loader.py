from __future__ import annotations

"""Load schema definitions from CSV files."""

import csv
import logging
from pathlib import Path
from typing import Any, Dict

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

VALID_TYPES = {"integer", "decimal", "string", "boolean", "datetime", "date", "text"}


def load_schema(path: str | Path = Path("config/schema_definitions.csv")) -> Dict[str, Dict[str, Dict[str, Any]]]:
    """Return schema definitions loaded from ``path``.

    The CSV must contain the columns defined in :data:`CSV_COLUMNS`.
    Duplicate ``table_name``/``field_name`` pairs or invalid types raise
    ``ValueError``.
    """

    csv_path = Path(path)
    if not csv_path.is_file():
        raise FileNotFoundError(csv_path)

    schema: Dict[str, Dict[str, Dict[str, Any]]] = {}
    with csv_path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        missing = [c for c in CSV_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"Missing columns: {', '.join(missing)}")

        for row in reader:
            table = row["table_name"].strip()
            field = row["field_name"].strip()
            ftype = row["type"].strip().lower()
            if ftype not in VALID_TYPES:
                raise ValueError(f"Invalid type '{ftype}' for {table}.{field}")
            if table not in schema:
                schema[table] = {}
            if field in schema[table]:
                raise ValueError(f"Duplicate field {table}.{field}")
            schema[table][field] = {
                "type": ftype,
                "precision": row.get("precision", "").strip() or None,
                "scale": row.get("scale", "").strip() or None,
                "required": row.get("required", "").strip().upper() == "TRUE",
                "default": row.get("default", "").strip() or None,
            }
    logger.info("Loaded schema with %d tables", len(schema))
    return schema
