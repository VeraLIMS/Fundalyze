import logging
from typing import Dict, Tuple

import pandas as pd
import yfinance as yf

logger = logging.getLogger(__name__)

ESSENTIAL_COLS = ["longName", "sector", "industry", "marketCap", "website"]


def fetch_profile_openbb(symbol: str) -> pd.DataFrame:
    """Fetch company profile via OpenBB. Returns empty DataFrame on error."""
    try:
        from openbb import obb  # imported lazily to avoid heavy startup if unused
        obj = obb.equity.profile(symbol=symbol)
        df = obj.to_df()
        return df
    except Exception as exc:
        logger.error("OpenBB profile fetch error for %s: %s", symbol, exc)
        return pd.DataFrame()


def fetch_profile_yf(symbol: str) -> pd.DataFrame:
    """Fetch company profile via yfinance. Returns empty DataFrame on error."""
    ticker = yf.Ticker(symbol)
    try:
        info = ticker.get_info()
    except Exception as exc:
        logger.error("yfinance info error for %s: %s", symbol, exc)
        return pd.DataFrame()
    if not info:
        return pd.DataFrame()
    return pd.DataFrame([info])


def is_complete(df: pd.DataFrame) -> bool:
    """Return True if DataFrame has essential columns and is non-empty."""
    if df is None or df.empty:
        return False
    return all(col in df.columns and df[col].notna().any() for col in ESSENTIAL_COLS)


def diff_dict(d1: Dict, d2: Dict) -> Dict[str, Tuple]:
    """Return dictionary of differing keys and their values."""
    out = {}
    keys = set(d1.keys()) | set(d2.keys())
    for k in keys:
        v1 = d1.get(k)
        v2 = d2.get(k)
        if v1 != v2:
            out[k] = (v1, v2)
    return out


def interactive_profile(symbol: str) -> pd.DataFrame:
    """Fetch profile from OpenBB and yfinance, compare and prompt user to choose."""
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
    d1 = obb_df.iloc[0].to_dict()
    d2 = yf_df.iloc[0].to_dict()
    diffs = diff_dict({k: d1.get(k) for k in ESSENTIAL_COLS}, {k: d2.get(k) for k in ESSENTIAL_COLS})
    if diffs:
        print(f"\nDifferences for {symbol}:")
        for k, (v1, v2) in diffs.items():
            print(f"  {k}: OpenBB='{v1}'  vs  yfinance='{v2}'")
    else:
        print(f"No differences detected for {symbol} on essential fields.")

    choice = input("Use OpenBB data (O) or yfinance data (Y)? [O/Y]: ").strip().lower()
    if choice == 'y':
        return yf_df
    return obb_df

