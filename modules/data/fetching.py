"""Utility functions for retrieving financial data."""

from __future__ import annotations

import pandas as pd
import requests
import yfinance as yf

from modules.config_utils import add_fmp_api_key
from modules.utils.progress_utils import progress_iter

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


def _parse_yf_info(info: dict, ticker: str) -> dict:
    """Return BASIC_FIELDS dict from yfinance info dict."""
    return {
        "Ticker": ticker.upper(),
        "Name": info.get("longName", ""),
        "Sector": resolve_term(info.get("sector", "")),
        "Industry": resolve_term(info.get("industry", "")),
        "Current Price": info.get("currentPrice", pd.NA),
        "Market Cap": info.get("marketCap", pd.NA),
        "PE Ratio": info.get("trailingPE", pd.NA),
        "Dividend Yield": info.get("dividendYield", pd.NA),
    }


def _fetch_from_fmp(ticker: str) -> dict:
    """Return BASIC_FIELDS dict using the FMP profile endpoint."""
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
        "Current Price": row.get("price", pd.NA),
        "Market Cap": row.get("mktCap", pd.NA),
        "PE Ratio": row.get("pe", pd.NA),
        "Dividend Yield": row.get("lastDiv", pd.NA),
    }


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

    if provider not in {"auto", "yf", "fmp"}:
        raise ValueError("provider must be 'auto', 'yf', or 'fmp'")

    if provider in {"auto", "yf"}:
        ticker_obj = yf.Ticker(ticker)
        try:
            info = ticker_obj.get_info()
        except Exception:
            info = {}
        if info and info.get("longName") is not None:
            return _parse_yf_info(info, ticker)
        if provider == "yf" and not info:
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

    rows = []
    total = len(tickers)

    def _worker(args):
        idx, tk = args
        if progress and max_workers in (None, 0, 1):
            print(f"[{idx}/{total}] Fetching {tk}...")
        return fetch_basic_stock_data(tk, fallback=fallback, provider=provider)

    if max_workers and max_workers > 1:
        from concurrent.futures import ThreadPoolExecutor

        iterator = enumerate(tickers, start=1)
        if progress:
            iterator = progress_iter(iterator, description="Tickers")

        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            rows = list(ex.map(_worker, iterator))
    else:
        iterator = enumerate(tickers, start=1)
        if progress:
            iterator = progress_iter(iterator, description="Tickers")
        for idx, tk in iterator:
            rows.append(_worker((idx, tk)))

    return pd.DataFrame(rows, columns=BASIC_FIELDS)
