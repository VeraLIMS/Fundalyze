"""Utility helpers for pandas data processing."""

from __future__ import annotations

import pandas as pd
from pathlib import Path
from typing import Optional, Any
import json


def strip_timezones(df: pd.DataFrame) -> pd.DataFrame:
    """Return copy of ``df`` with timezone information removed."""
    if df is None:
        return df
    result = df.copy()
    if isinstance(result.index, pd.DatetimeIndex) and result.index.tz is not None:
        result.index = result.index.tz_localize(None)
    for col in result.select_dtypes(include=["datetimetz"]).columns:
        result[col] = result[col].dt.tz_localize(None)
    return result


def ensure_period_column(df: pd.DataFrame, column_name: str = "Period") -> pd.DataFrame:
    """Ensure ``df`` has a period column by resetting index if needed."""
    if column_name not in df.columns:
        df = df.reset_index().rename(columns={"index": column_name})
    return df


def read_csv_if_exists(path: Path, **kwargs) -> Optional[pd.DataFrame]:
    """Return DataFrame from ``path`` if the file exists else ``None``."""
    if path.exists():
        try:
            return pd.read_csv(path, **kwargs)
        except Exception:
            return None
    return None


def read_json_if_exists(path: Path) -> Optional[Any]:
    """Return deserialized JSON object from ``path`` if it exists."""
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None
