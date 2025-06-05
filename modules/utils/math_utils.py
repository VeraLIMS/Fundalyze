from __future__ import annotations

"""Mathematical helper utilities.

These functions are intentionally small so they can be imported directly::

    from modules.utils import moving_average
    ma = moving_average(series, window=30)
"""

import pandas as pd


def moving_average(series: pd.Series, window: int) -> pd.Series:
    """Return rolling mean over ``window`` periods."""
    if series is None or series.empty:
        return pd.Series(dtype="float64")
    return series.rolling(window=window, min_periods=1).mean()


def percentage_change(series: pd.Series, periods: int = 1) -> pd.Series:
    """Return percent change from ``periods`` prior values."""
    if series is None or series.empty:
        return pd.Series(dtype="float64")
    return series.pct_change(periods=periods, fill_method=None)
