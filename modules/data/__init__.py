"""Unified access to common data helpers.

This package exposes a selection of frequently used functions from the
individual submodules so callers can simply ``import data`` and reference
them directly.  All submodules remain importable on their own.
"""

from .fetching import fetch_basic_stock_data, BASIC_FIELDS
from .directus_client import (
    list_collections,
    list_fields,
    fetch_items,
    fetch_items_filtered,
    insert_items,
    create_field,
    create_collection_if_missing,
    directus_request,
    reload_env,
)
from .term_mapper import load_mapping, save_mapping, resolve_term, add_alias
from .compare import interactive_profile, diff_dict
from .directus_mapper import (
    load_field_map,
    save_field_map,
    prepare_records,
    interactive_prepare_records,
    refresh_field_map,
    ensure_field_mapping,
)
from .unified_fetcher import fetch_company_data, fetch_and_store

__all__ = [
    "fetch_basic_stock_data",
    "BASIC_FIELDS",
    "list_collections",
    "list_fields",
    "fetch_items",
    "fetch_items_filtered",
    "insert_items",
    "create_field",
    "create_collection_if_missing",
    "directus_request",
    "reload_env",
    "load_mapping",
    "save_mapping",
    "resolve_term",
    "add_alias",
    "interactive_profile",
    "diff_dict",
    "load_field_map",
    "save_field_map",
    "prepare_records",
    "interactive_prepare_records",
    "refresh_field_map",
    "ensure_field_mapping",
    "fetch_company_data",
    "fetch_and_store",
]
