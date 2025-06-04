"""Utility functions for retrieving financial data."""

from __future__ import annotations

import pandas as pd
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


def fetch_basic_stock_data(ticker: str) -> dict:
    """Fetch key fundamental data for a ticker via yfinance."""
    ticker_obj = yf.Ticker(ticker)
    info = ticker_obj.info
    if not info or "longName" not in info or info["longName"] is None:
        raise ValueError("No valid data returned by yfinance.")
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
