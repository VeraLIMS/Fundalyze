"""Utilities for comparing company profiles from OpenBB and yfinance."""

from __future__ import annotations

import logging
import sys
from typing import Any, Dict, Tuple

import pandas as pd
import yfinance as yf
from modules.utils import get_openbb

logger = logging.getLogger(__name__)

# Core company profile fields we expect from data sources
ESSENTIAL_COLS: list[str] = [
    "longName",
    "sector",
    "industry",
    "marketCap",
    "website",
]

PROMPT_MSG = "Use OpenBB data (O) or yfinance data (Y)? [O/Y]: "


def fetch_profile_openbb(symbol: str) -> pd.DataFrame:
    """Return a company profile from OpenBB.

    Parameters
    ----------
    symbol:
        The ticker symbol to query.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the profile or empty on failure.
    """
    try:
        obb = get_openbb()
        obj = obb.equity.profile(symbol=symbol)
        return obj.to_df()
    except Exception as exc:  # pragma: no cover - network errors
        logger.error("OpenBB profile fetch error for %s: %s", symbol, exc)
        return pd.DataFrame()


def fetch_profile_yf(symbol: str) -> pd.DataFrame:
    """Return a company profile from yfinance.

    Parameters
    ----------
    symbol:
        The ticker symbol to query.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the profile or empty on failure.
    """
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
    """Return ``True`` if *df* contains all essential columns with any values."""

    if df is None or df.empty:
        return False
    return all(col in df.columns and df[col].notna().any() for col in ESSENTIAL_COLS)


def diff_dict(d1: Dict, d2: Dict) -> Dict[str, Tuple[Any, Any]]:
    """Return dictionary of differing keys and their corresponding values."""

    return {
        k: (d1.get(k), d2.get(k)) for k in set(d1) | set(d2) if d1.get(k) != d2.get(k)
    }


def compare_profiles(
    obb_df: pd.DataFrame, yf_df: pd.DataFrame
) -> Dict[str, Tuple[Any, Any]]:
    """Return differences between two profile DataFrames using ``ESSENTIAL_COLS``."""

    d1 = obb_df.iloc[0].to_dict() if not obb_df.empty else {}
    d2 = yf_df.iloc[0].to_dict() if not yf_df.empty else {}
    return diff_dict(
        {k: d1.get(k) for k in ESSENTIAL_COLS}, {k: d2.get(k) for k in ESSENTIAL_COLS}
    )


def _show_differences(symbol: str, diffs: Dict[str, Tuple[Any, Any]]) -> None:
    """Pretty-print profile differences for ``symbol``."""

    if diffs:
        print(f"\nDifferences for {symbol}:")
        for key, (v1, v2) in diffs.items():
            print(f"  {key}: OpenBB='{v1}'  vs  yfinance='{v2}'")
    else:
        print(f"No differences detected for {symbol} on essential fields.")


def interactive_profile(symbol: str) -> pd.DataFrame:
    """Interactively choose between OpenBB and yfinance profile data.

    Both data sources are queried. If only one returns a complete profile it is
    used automatically. When both provide profiles, the differences are shown and
    the user is asked which dataset to keep.
    """
    obb_df = fetch_profile_openbb(symbol)
    yf_df = fetch_profile_yf(symbol)

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
    diffs = compare_profiles(obb_df, yf_df)
    _show_differences(symbol, diffs)

    choice = input(PROMPT_MSG).strip().lower()
    if choice == "y":
        return yf_df
    return obb_df


def _main(argv: list[str]) -> int:
    """Run module as a script.

    Parameters
    ----------
    argv:
        Command-line arguments.
    """
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
