"""Simple portfolio and group analysis utilities."""
from __future__ import annotations

import pandas as pd


def portfolio_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return basic summary statistics for numeric columns."""
    if df is None or df.empty:
        return pd.DataFrame()
    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    if not numeric_cols:
        return pd.DataFrame()
    summary = df[numeric_cols].describe().loc[["mean", "min", "max"]]
    return summary


def sector_counts(df: pd.DataFrame) -> pd.DataFrame:
    """Return count of tickers per sector."""
    if df is None or df.empty or "Sector" not in df.columns:
        return pd.DataFrame()
    counts = df["Sector"].fillna("Unknown").value_counts().rename_axis("Sector")
    return counts.reset_index(name="Count")


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Return Pearson correlation matrix for numeric columns."""
    if df is None or df.empty:
        return pd.DataFrame()
    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    if len(numeric_cols) < 2:
        return pd.DataFrame()
    return df[numeric_cols].corr()


def moving_average(series: pd.Series, window: int) -> pd.Series:
    """Return rolling mean over ``window`` periods."""

    if series is None or series.empty:
        return pd.Series(dtype="float64")
    return series.rolling(window=window, min_periods=1).mean()
