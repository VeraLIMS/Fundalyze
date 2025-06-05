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
    insert_items,
    create_field,
    directus_request,
    reload_env,
)
from .term_mapper import load_mapping, save_mapping, resolve_term, add_alias
from .compare import interactive_profile, diff_dict
from .directus_mapper import (
    load_field_map,
    save_field_map,
    prepare_records,
    refresh_field_map,
    ensure_field_mapping,
)

__all__ = [
    "fetch_basic_stock_data",
    "BASIC_FIELDS",
    "list_collections",
    "list_fields",
    "fetch_items",
    "insert_items",
    "create_field",
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
    "refresh_field_map",
    "ensure_field_mapping",
]
