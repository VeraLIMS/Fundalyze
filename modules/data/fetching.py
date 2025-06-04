"""Utility functions for retrieving financial data."""

from __future__ import annotations

import pandas as pd
import requests
import yfinance as yf

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
    """Return BASIC_FIELDS dict using FMP profile endpoint."""
    url = FMP_PROFILE_URL.format(symbol=ticker)
    resp = requests.get(url)
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


def fetch_basic_stock_data(ticker: str, *, fallback: bool = True) -> dict:
    """Fetch key fundamental data for a ticker via yfinance with optional FMP fallback."""
    ticker_obj = yf.Ticker(ticker)
    try:
        info = ticker_obj.get_info()
    except Exception:
        info = {}
    if info and info.get("longName") is not None:
        return _parse_yf_info(info, ticker)
    if not fallback:
        raise ValueError("No valid data returned by yfinance.")
    fmp_data = _fetch_from_fmp(ticker)
    if not fmp_data:
        raise ValueError("No valid data returned by yfinance or FMP.")
    return fmp_data
