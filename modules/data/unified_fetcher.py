from __future__ import annotations

"""Unified data fetching with prioritized fallbacks."""

import logging
from typing import Any, Dict, Iterable

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
            logger.info("OpenBB returned no data for %s", ticker)
            return None
        row = df.iloc[0]
        data = {
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
        logger.info("Fetched data for %s from OpenBB", ticker)
        return data
    except Exception as exc:  # pragma: no cover - network failure
        logger.warning("OpenBB fetch failed for %s: %s", ticker, exc)
        return None


DEFAULT_USE_OPENBB = True


def _log_missing(data: Dict[str, Any], fields: Iterable[str], ticker: str) -> None:
    missing = []
    for f in fields:
        val = data.get(f)
        if val is pd.NA or val is None or val == "":
            missing.append(f)
    if missing:
        logger.warning("%s missing fields: %s", ticker, ", ".join(missing))


def fetch_company_data(ticker: str, *, use_openbb: bool | None = None) -> Dict[str, Any] | None:
    """Return normalized company data using prioritized sources."""
    if use_openbb is None:
        use_openbb = DEFAULT_USE_OPENBB

    data = _from_openbb(ticker) if use_openbb else None
    source = "OpenBB" if data else "yfinance/FMP"
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
            cleaned = {}
            for k, v in data.items():
                if v is pd.NA or v is None or v == "":
                    continue
                cleaned[k] = v
            merged = yf_data | cleaned
            _log_missing(merged, yf_data.keys(), ticker)
            data = merged
        except Exception as exc:
            logger.info("Fallback fetch failed for %s: %s", ticker, exc)

    # Normalize sector/industry
    if data:
        if "Sector" in data:
            data["Sector"] = resolve_term(str(data.get("Sector", "")))
        if "Industry" in data:
            data["Industry"] = resolve_term(str(data.get("Industry", "")))
    logger.info("Fetched %s using %s", ticker, source)
    return data


def fetch_and_store(
    ticker: str,
    collection: str = "company_profiles",
    *,
    use_openbb: bool | None = None,
) -> Dict[str, Any] | None:
    """Fetch data for ``ticker`` and insert into Directus."""
    record = fetch_company_data(ticker, use_openbb=use_openbb)
    if not record:
        return None
    prepared = prepare_records(collection, [record])
    try:
        insert_items(collection, prepared)
    except Exception as exc:  # pragma: no cover - network failure
        logger.error("Directus insertion failed: %s", exc)
    return record
