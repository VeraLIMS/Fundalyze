#!/usr/bin/env python3
"""Verify field mappings and optionally insert records into Directus.

This script checks that all keys in a JSON dataset have a corresponding
mapping for the given Directus collection. It logs any missing mappings or
fields that do not exist in the target collection. The records are then
converted using :func:`modules.data.directus_mapper.prepare_records`. If the
resulting mapped record is empty, an error is raised before attempting any
insertion.
"""
from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Any, Dict, Iterable, List

from modules.data import directus_mapper as dm
from modules.data.directus_client import insert_items, list_fields

logger = logging.getLogger(__name__)


def load_records(path: str) -> List[Dict[str, Any]]:
    """Return list of record dictionaries from ``path``."""
    data = json.loads(Path(path).read_text())
    if isinstance(data, dict):
        return [data]
    if isinstance(data, list) and all(isinstance(r, dict) for r in data):
        return data
    raise ValueError("JSON must be an object or list of objects")


def verify_mapping(collection: str, records: Iterable[Dict[str, Any]]) -> bool:
    """Check mapping configuration for ``collection`` against ``records``."""
    mapping = dm.load_field_map().get("collections", {}).get(collection, {}).get("fields", {})
    try:
        allowed = set(list_fields(collection))
    except Exception as exc:  # pragma: no cover - network
        logger.warning("Could not fetch fields from Directus: %s", exc)
        allowed = set()

    ok = True
    for row in records:
        for key in row.keys():
            entry = mapping.get(key)
            target = entry.get("mapped_to") if entry else None
            if target is None:
                logger.warning("[MISSING] '%s' not mapped for collection '%s'", key, collection)
                ok = False
            elif allowed and target not in allowed:
                logger.warning(
                    "[INVALID] mapping %s -> %s not in Directus fields", key, target
                )
                ok = False
    return ok


def main(argv: Iterable[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Validate Directus field mapping")
    parser.add_argument("collection", help="Directus collection name")
    parser.add_argument("json_file", help="Path to JSON file with record(s)")
    parser.add_argument("--insert", action="store_true", help="Insert mapped records")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug output")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(levelname)s: %(message)s")

    records = load_records(args.json_file)
    logger.info("Loaded %d record(s) from %s", len(records), args.json_file)

    valid = verify_mapping(args.collection, records)

    prepared = dm.prepare_records(args.collection, records, verbose=True)
    for rec in prepared:
        if not rec:
            raise ValueError("Mapped record is empty. Check field mappings.")

    logger.info("Prepared records: %s", prepared)

    if args.insert:
        if not valid:
            logger.warning("Skipping insert due to mapping issues.")
            return
        result = insert_items(args.collection, prepared)
        logger.info("Insert result: %s", result)


if __name__ == "__main__":
    main()
