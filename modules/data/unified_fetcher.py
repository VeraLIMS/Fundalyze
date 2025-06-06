from __future__ import annotations

"""Unified data fetching with prioritized fallbacks."""

import logging
from typing import Any, Dict

import pandas as pd

from .fetching import fetch_basic_stock_data
from .term_mapper import resolve_term
from .directus_mapper import prepare_records
from .directus_client import insert_items
from modules.utils import get_openbb

logger = logging.getLogger(__name__)


def _from_openbb(ticker: str) -> Dict[str, Any] | None:
    """Return company data from OpenBB or ``None`` on error."""
    try:
        obb = get_openbb()
        df = obb.equity.profile(symbol=ticker).to_df()
        if df.empty:
            return None
        row = df.iloc[0]
        return {
            "Ticker": ticker.upper(),
            "Name": row.get("name") or row.get("legal_name") or "",
            "Sector": row.get("sector") or "",
            "Industry": row.get("industry_category")
            or row.get("industry_group")
            or "",
            "Current Price": row.get("last_price", pd.NA),
            "Market Cap": row.get("market_cap", pd.NA),
            "PE Ratio": pd.NA,
            "Dividend Yield": row.get("dividend_yield", pd.NA),
        }
    except Exception as exc:  # pragma: no cover - network failure
        logger.warning("OpenBB fetch failed for %s: %s", ticker, exc)
        return None


def fetch_company_data(ticker: str) -> Dict[str, Any] | None:
    """Return normalized company data using prioritized sources."""
    data = _from_openbb(ticker)
    if not data:
        try:
            data = fetch_basic_stock_data(ticker)
        except Exception as exc:
            logger.error("All fetchers failed for %s: %s", ticker, exc)
            return None
    else:
        # fill missing fields with yfinance/FMP fallback
        try:
            yf_data = fetch_basic_stock_data(ticker)
            data = {**yf_data, **{k: v for k, v in data.items() if v not in ("", pd.NA)}}
        except Exception:
            pass

    # Normalize sector/industry
    if data:
        if "Sector" in data:
            data["Sector"] = resolve_term(str(data.get("Sector", "")))
        if "Industry" in data:
            data["Industry"] = resolve_term(str(data.get("Industry", "")))
    return data


def fetch_and_store(ticker: str, collection: str = "company_profiles") -> Dict[str, Any] | None:
    """Fetch data for ``ticker`` and insert into Directus."""
    record = fetch_company_data(ticker)
    if not record:
        return None
    prepared = prepare_records(collection, [record])
    try:
        insert_items(collection, prepared)
    except Exception as exc:  # pragma: no cover - network failure
        logger.error("Directus insertion failed: %s", exc)
    return record
