from __future__ import annotations

"""Fetch financial statements and insert them into Directus."""

import os
import logging
from typing import Iterable, Dict

import pandas as pd

from modules.utils import get_openbb, parse_number
from .directus_client import insert_items
from .directus_mapper import prepare_records

logger = logging.getLogger(__name__)

DEFAULT_STATEMENTS = ("income", "balance", "cash")

COLLECTION_MAP = {
    "income": "income_statement",
    "balance": "balance_sheet",
    "cash": "cash_flow",
}


def _fetch_statement(obb, ticker: str, stmt: str, period: str) -> pd.DataFrame:
    """Return statement DataFrame from OpenBB or empty DataFrame."""
    try:
        fn = getattr(obb.equity.fundamental, stmt)
        df = fn(symbol=ticker, period=period).to_df()
        if isinstance(df, pd.DataFrame):
            # Normalize numeric values
            return df.applymap(parse_number)
    except Exception as exc:  # pragma: no cover - network errors
        logger.warning("%s %s fetch failed for %s: %s", stmt, period, ticker, exc)
    return pd.DataFrame()


def fetch_statements(ticker: str, statements: Iterable[str] | None = None) -> Dict[str, Dict[str, pd.DataFrame]]:
    """Return financial statements for ``ticker`` grouped by statement and period."""
    if statements is None:
        statements = DEFAULT_STATEMENTS
    obb = get_openbb()
    data: Dict[str, Dict[str, pd.DataFrame]] = {}
    for stmt in statements:
        data[stmt] = {
            "annual": _fetch_statement(obb, ticker, stmt, "annual"),
            "quarter": _fetch_statement(obb, ticker, stmt, "quarter"),
        }
    return data


def _insert_dataframe(df: pd.DataFrame, collection: str) -> None:
    """Prepare and insert ``df`` rows into Directus collection."""
    if df.empty:
        return
    records = prepare_records(collection, df.reset_index().to_dict(orient="records"))
    try:
        insert_items(collection, records)
    except Exception as exc:  # pragma: no cover - network errors
        logger.error("Directus insertion failed for %s: %s", collection, exc)


def store_statements(data: Dict[str, Dict[str, pd.DataFrame]]) -> None:
    """Insert fetched statements into Directus using environment collection names."""
    for stmt, periods in data.items():
        base = COLLECTION_MAP.get(stmt, stmt)
        collection = os.getenv(f"DIRECTUS_{base.upper()}_COLLECTION", base)
        for period, df in periods.items():
            if not df.empty:
                df = df.copy()
                df.insert(0, "period", df.index)
                _insert_dataframe(df, collection)


def fetch_and_store_statements(
    ticker: str, *, statements: Iterable[str] | None = None
) -> Dict[str, Dict[str, pd.DataFrame]]:
    """Fetch financial statements for ``ticker`` and store them in Directus."""
    data = fetch_statements(ticker, statements)
    store_statements(data)
    return data
