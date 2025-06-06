from __future__ import annotations

"""Synchronize schema definitions between CSV and Directus."""

import logging
from typing import Any, Dict

from modules.api.directus_client import DirectusClient
from .schema_loader import load_schema
from .schema_exporter import fetch_schema

logger = logging.getLogger(__name__)


def _fields_equal(csv_def: Dict[str, Any], directus_def: Dict[str, Any]) -> bool:
    """Return ``True`` if ``csv_def`` matches ``directus_def``."""
    def norm(val: Any) -> Any:
        if val is None:
            return None
        if isinstance(val, str):
            return val.strip()
        return val

    return (
        norm(csv_def.get("type")) == norm(directus_def.get("type"))
        and norm(csv_def.get("precision")) == norm(directus_def.get("precision"))
        and norm(csv_def.get("scale")) == norm(directus_def.get("scale"))
        and bool(csv_def.get("required"))
        == (not directus_def.get("schema", {}).get("is_nullable", True))
        and norm(csv_def.get("default")) == norm(directus_def.get("default_value"))
    )


def sync_schema(
    csv_path: str | None = None,
    client: DirectusClient | None = None,
    *,
    remove_extra: bool = False,
) -> None:
    """Synchronize ``csv_path`` definitions with Directus."""
    client = client or DirectusClient()
    csv_schema = load_schema(csv_path or "config/schema_definitions.csv")
    directus_schema = fetch_schema(client)

    # CSV -> Directus
    for table, fields in csv_schema.items():
        d_fields = directus_schema.get(table, {})
        for field, csv_def in fields.items():
            if field in d_fields:
                if not _fields_equal(csv_def, d_fields[field]):
                    client.update_field(table, field, csv_def)
                    logger.info("[SYNC][UPDATE] %s.%s", table, field)
                else:
                    logger.debug("[SYNC][SKIP] %s.%s", table, field)
            else:
                client.create_field(table, field, csv_def)
                logger.info("[SYNC][CREATE] %s.%s", table, field)

    # Handle extra fields
    if remove_extra:
        for table, fields in directus_schema.items():
            if table in csv_schema:
                for field in fields:
                    if field not in csv_schema[table]:
                        client.delete_field(table, field)
                        logger.info("[SYNC][DELETE] %s.%s", table, field)
