"""Utilities for comparing company profiles from OpenBB and yfinance."""

from __future__ import annotations

import logging
import sys
from typing import Dict, Tuple, Any

import pandas as pd
import yfinance as yf

from modules.utils import get_openbb

logger = logging.getLogger(__name__)

ESSENTIAL_COLS = ["longName", "sector", "industry", "marketCap", "website"]


def fetch_profile_openbb(symbol: str) -> pd.DataFrame:
    """Return company profile data via OpenBB or an empty DataFrame on error."""

    try:
        obb = get_openbb()
        obj = obb.equity.profile(symbol=symbol)
        return obj.to_df()
    except Exception as exc:  # pragma: no cover - network errors
        logger.error("OpenBB profile fetch error for %s: %s", symbol, exc)
        return pd.DataFrame()


def fetch_profile_yf(symbol: str) -> pd.DataFrame:
    """Return company profile via yfinance or an empty DataFrame on error."""

    ticker = yf.Ticker(symbol)
    try:
        info = ticker.get_info()
    except Exception as exc:  # pragma: no cover - network errors
        logger.error("yfinance info error for %s: %s", symbol, exc)
        return pd.DataFrame()
    if not info:
        return pd.DataFrame()
    return pd.DataFrame([info])


def is_complete(df: pd.DataFrame) -> bool:
    """Return ``True`` if ``df`` contains required columns with at least one value."""

    if df is None or df.empty:
        return False

    return all(col in df.columns and df[col].notna().any() for col in ESSENTIAL_COLS)


def diff_dict(d1: Dict[str, Any], d2: Dict[str, Any]) -> Dict[str, Tuple[Any, Any]]:
    """Return mapping of keys with differing values in ``d1`` and ``d2``."""

    keys = set(d1) | set(d2)
    return {k: (d1.get(k), d2.get(k)) for k in keys if d1.get(k) != d2.get(k)}


def _show_differences(symbol: str, diffs: Dict[str, Tuple[Any, Any]]) -> None:
    """Print human-readable differences between profile dictionaries."""

    if not diffs:
        print(f"No differences detected for {symbol} on essential fields.")
        return

    print(f"\nDifferences for {symbol}:")
    for key, (v1, v2) in diffs.items():
        print(f"  {key}: OpenBB='{v1}'  vs  yfinance='{v2}'")


def interactive_profile(symbol: str) -> pd.DataFrame:
    """Fetch profiles from both sources and prompt the user to choose."""

    obb_df = fetch_profile_openbb(symbol)
    yf_df = fetch_profile_yf(symbol)

    return _select_preferred_profile(symbol, obb_df, yf_df)


def _select_preferred_profile(
    symbol: str, obb_df: pd.DataFrame, yf_df: pd.DataFrame
) -> pd.DataFrame:
    """Return the chosen profile DataFrame based on completeness and user input."""

    obb_complete = is_complete(obb_df)
    yf_complete = is_complete(yf_df)

    if not obb_complete and not yf_complete:
        logger.warning("Both OpenBB and yfinance failed to return complete data.")
        return pd.DataFrame()

    if obb_complete and not yf_complete:
        logger.info("Using OpenBB data for %s", symbol)
        return obb_df

    if yf_complete and not obb_complete:
        logger.info("Using yfinance data for %s", symbol)
        return yf_df

    # Both have data, compare
    diffs = diff_dict(
        {k: obb_df.iloc[0].get(k) for k in ESSENTIAL_COLS},
        {k: yf_df.iloc[0].get(k) for k in ESSENTIAL_COLS},
    )
    _show_differences(symbol, diffs)

    choice = input("Use OpenBB data (O) or yfinance data (Y)? [O/Y]: ").strip().lower()
    return yf_df if choice == "y" else obb_df


def _main(argv: list[str]) -> int:
    """Console entry point used by ``python -m data.compare``."""

    if len(argv) != 2:
        print("Usage: python -m data.compare <TICKER>")
        return 1

    symbol = argv[1].upper()
    df = interactive_profile(symbol)
    if df.empty:
        print("No data available.")
        return 1

    print(df.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv))

