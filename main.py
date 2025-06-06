#!/usr/bin/env python3
from __future__ import annotations

"""Entry point for schema synchronization utilities."""

import argparse

from modules.logging_utils import setup_logging
from modules.api import DirectusClient
from modules.schema import export_schema, sync_schema


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Directus schema utilities")
    sub = parser.add_subparsers(dest="command", required=True)

    exp = sub.add_parser("export", help="Export Directus schema to CSV")
    exp.add_argument(
        "--output",
        default="config/schema_definitions_export.csv",
        help="Destination CSV file",
    )

    sync = sub.add_parser("sync", help="Sync CSV schema to Directus")
    sync.add_argument(
        "--csv",
        default="config/schema_definitions.csv",
        help="CSV file with schema definitions",
    )
    sync.add_argument(
        "--delete-extra",
        action="store_true",
        help="Delete fields not defined in CSV",
    )

    return parser.parse_args()


def main() -> None:
    setup_logging("logs/schema_sync.log")
    args = parse_args()
    client = DirectusClient()
    if args.command == "export":
        export_schema(client, args.output)
    elif args.command == "sync":
        sync_schema(args.csv, client, remove_extra=args.delete_extra)


if __name__ == "__main__":
    main()
