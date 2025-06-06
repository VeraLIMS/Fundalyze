#!/usr/bin/env python3
"""CLI to append missing keys to directus_field_map.json."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import modules.data.directus_mapper as dm


def parse_args(args=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Add missing field mappings based on provided records"
    )
    parser.add_argument("collection", help="Directus collection name")
    parser.add_argument("json_file", help="Path to JSON file with record(s)")
    return parser.parse_args(args)


def load_records(path: str):
    data = json.loads(Path(path).read_text())
    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        return data
    raise ValueError("JSON must be an object or list of objects")


def main(argv=None) -> None:
    args = parse_args(argv)
    records = load_records(args.json_file)
    dm.add_missing_mappings(args.collection, records)
    print("directus_field_map.json updated with new keys, if any.")


if __name__ == "__main__":
    main()
