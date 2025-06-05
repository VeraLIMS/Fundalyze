"""Utility functions for quick portfolio analytics.

This module bundles a few generic helpers that are reused across the
command-line tools.  The goal is to keep these functions dependency free and
easy to compose in notebooks or other Python scripts.

Available utilities
-------------------
``portfolio_summary``
    Compute mean/min/max statistics for the numeric columns of a DataFrame.
``sector_counts``
    Count the number of tickers by sector.
``correlation_matrix``
    Return a Pearson correlation matrix for the numeric columns.

Additionally the rolling ``moving_average`` and ``percentage_change`` helpers
are re-exported from :mod:`modules.utils.math_utils` for convenience.
"""
from __future__ import annotations

import pandas as pd
from modules.utils.math_utils import moving_average, percentage_change

__all__ = [
    "portfolio_summary",
    "sector_counts",
    "correlation_matrix",
    "moving_average",
    "percentage_change",
]


def portfolio_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return basic summary statistics for numeric columns.

    Parameters
    ----------
    df:
        DataFrame containing portfolio data.

    Returns
    -------
    pd.DataFrame
        A DataFrame with the mean, minimum and maximum for each numeric column.
        An empty DataFrame is returned when ``df`` has no numeric data.
    """
    if df is None or df.empty:
        return pd.DataFrame()
    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    if not numeric_cols:
        return pd.DataFrame()
    summary = df[numeric_cols].describe().loc[["mean", "min", "max"]]
    return summary


def sector_counts(df: pd.DataFrame) -> pd.DataFrame:
    """Return count of tickers per sector.

    Parameters
    ----------
    df:
        Portfolio DataFrame expected to contain a ``"Sector"`` column.

    Returns
    -------
    pd.DataFrame
        Two-column DataFrame ``["Sector", "Count"]`` sorted by frequency. An
        empty DataFrame is returned when sector information is unavailable.
    """
    if df is None or df.empty or "Sector" not in df.columns:
        return pd.DataFrame()
    counts = df["Sector"].fillna("Unknown").value_counts().rename_axis("Sector")
    return counts.reset_index(name="Count")


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Return Pearson correlation matrix for numeric columns.

    Parameters
    ----------
    df:
        DataFrame with numeric columns to correlate.

    Returns
    -------
    pd.DataFrame
        Square correlation matrix or an empty DataFrame when fewer than two
        numeric columns exist.
    """
    if df is None or df.empty:
        return pd.DataFrame()
    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    if len(numeric_cols) < 2:
        return pd.DataFrame()
    return df[numeric_cols].corr()


