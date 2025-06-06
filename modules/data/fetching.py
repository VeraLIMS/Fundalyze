"""Utility functions for retrieving financial data."""

from __future__ import annotations

from typing import Any, Iterable, Mapping

import pandas as pd
import requests
import yfinance as yf

from modules.config_utils import add_fmp_api_key
from modules.utils.progress_utils import progress_iter
from modules.utils import parse_number

from .term_mapper import resolve_term

BASIC_FIELDS = [
    "Ticker",
    "Name",
    "Sector",
    "Industry",
    "Current Price",
    "Market Cap",
    "PE Ratio",
    "Dividend Yield",
]


FMP_PROFILE_URL = "https://financialmodelingprep.com/api/v3/profile/{symbol}"
FMP_TIMEOUT = 10

_PROVIDERS = {"auto", "yf", "fmp"}


def _parse_yf_info(info: Mapping[str, Any], ticker: str) -> dict[str, Any]:
    """Convert ``info`` from yfinance into the :data:`BASIC_FIELDS` format."""
    return {
        "Ticker": ticker.upper(),
        "Name": info.get("longName", ""),
        "Sector": resolve_term(info.get("sector", "")),
        "Industry": resolve_term(info.get("industry", "")),
        "Current Price": parse_number(info.get("currentPrice", pd.NA)),
        "Market Cap": parse_number(info.get("marketCap", pd.NA)),
        "PE Ratio": parse_number(info.get("trailingPE", pd.NA)),
        "Dividend Yield": parse_number(info.get("dividendYield", pd.NA)),
    }


def _fetch_from_fmp(ticker: str) -> dict[str, Any]:
    """Return :data:`BASIC_FIELDS` information using the FMP profile endpoint."""
    url = add_fmp_api_key(FMP_PROFILE_URL.format(symbol=ticker))
    resp = requests.get(url, timeout=FMP_TIMEOUT)
    resp.raise_for_status()
    data = resp.json()
    if not data or not isinstance(data, list):
        return {}
    row = data[0]
    return {
        "Ticker": ticker.upper(),
        "Name": row.get("companyName", ""),
        "Sector": resolve_term(row.get("sector", "")),
        "Industry": resolve_term(row.get("industry", "")),
        "Current Price": parse_number(row.get("price", pd.NA)),
        "Market Cap": parse_number(row.get("mktCap", pd.NA)),
        "PE Ratio": parse_number(row.get("pe", pd.NA)),
        "Dividend Yield": parse_number(row.get("lastDiv", pd.NA)),
    }


def _fetch_from_yf(ticker: str) -> dict[str, Any] | None:
    """Return :data:`BASIC_FIELDS` information from yfinance or ``None``."""
    ticker_obj = yf.Ticker(ticker)
    try:
        info = ticker_obj.get_info()
    except Exception:
        return None
    if info and info.get("longName") is not None:
        return _parse_yf_info(info, ticker)
    return None


def fetch_basic_stock_data(
    ticker: str,
    *,
    fallback: bool = True,
    provider: str = "auto",
) -> dict:
    """Fetch key fundamental data for a ticker.

    Parameters
    ----------
    ticker:
        Stock symbol to fetch.
    fallback:
        When ``provider='auto'`` and yfinance returns incomplete data,
        query FMP as a secondary source.
    provider:
        ``'yf'`` to use yfinance only, ``'fmp'`` for FMP only,
        or ``'auto'`` (default) to try yfinance then FMP if ``fallback``.
    """

    provider = provider.lower()

    if provider not in _PROVIDERS:
        raise ValueError("provider must be 'auto', 'yf', or 'fmp'")

    if provider in {"auto", "yf"}:
        yf_data = _fetch_from_yf(ticker)
        if yf_data is not None:
            return yf_data
        if provider == "yf":
            raise ValueError("No valid data returned by yfinance.")

    if provider in {"auto", "fmp"} and fallback:
        fmp_data = _fetch_from_fmp(ticker)
        if fmp_data:
            return fmp_data
        if provider == "fmp":
            raise ValueError("No valid data returned by FMP.")

    raise ValueError("No valid data returned by yfinance or FMP.")


def fetch_basic_stock_data_batch(
    tickers: list[str] | tuple[str, ...],
    *,
    fallback: bool = True,
    provider: str = "auto",
    dedup: bool = False,
    progress: bool = False,
    max_workers: int | None = None,
) -> pd.DataFrame:
    """Fetch :func:`fetch_basic_stock_data` for multiple tickers.

    Parameters
    ----------
    tickers:
        Iterable of ticker symbols.
    fallback:
        Passed through to :func:`fetch_basic_stock_data`.
    provider:
        Data source to use: ``"auto"`` (default), ``"yf"`` or ``"fmp"``.

    dedup:
        If ``True``, remove duplicate symbols before fetching.
    progress:
        When ``True`` display a progress bar while fetching. The bar works for
        both sequential and parallel execution.
    max_workers:
        If greater than 1, fetch tickers in parallel using ``ThreadPoolExecutor``.

    Returns
    -------
    pandas.DataFrame
        DataFrame with one row per ticker and columns defined in
        :data:`BASIC_FIELDS`.
    """

    if dedup:
        tickers = list(dict.fromkeys(tickers))

    if not tickers:
        return pd.DataFrame(columns=BASIC_FIELDS)

    rows: list[dict[str, Any]] = []
    total = len(tickers)

    def _worker(args: tuple[int, str]) -> dict[str, Any]:
        idx, tk = args
        if progress and max_workers in (None, 0, 1):
            print(f"[{idx}/{total}] Fetching {tk}...")
        return fetch_basic_stock_data(tk, fallback=fallback, provider=provider)

    if max_workers and max_workers > 1:
        from concurrent.futures import ThreadPoolExecutor

        iterator: Iterable[tuple[int, str]] = enumerate(tickers, start=1)
        if progress:
            iterator = progress_iter(iterator, description="Tickers")

        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            rows = list(ex.map(_worker, iterator))
    else:
        iterator: Iterable[tuple[int, str]] = enumerate(tickers, start=1)
        if progress:
            iterator = progress_iter(iterator, description="Tickers")
        for item in iterator:
            rows.append(_worker(item))

    return pd.DataFrame(rows, columns=BASIC_FIELDS)
