"""Utility helpers for pandas data processing.

These functions provide small wrappers around common ``pandas`` operations
so callers do not have to repeat error handling.  Typical usage::

    from pathlib import Path
    from modules.utils import read_csv_if_exists, strip_timezones

    df = read_csv_if_exists(Path("prices.csv"))
    if df is not None:
        df = strip_timezones(df)
"""

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


def write_dataframe(
    df: pd.DataFrame,
    csv_path: Path,
    *,
    write_csv: bool = True,
    write_json: bool = False,
) -> None:
    """Save ``df`` to CSV and/or JSON using ``csv_path`` as base path."""

    if write_csv:
        df.to_csv(csv_path, index=False)

    if write_json:
        json_path = csv_path.with_suffix(".json")
        df.to_json(json_path, orient="records", indent=2, date_format="iso")


def parse_number(val: Any) -> Any:
    """Return numeric value parsed from ``val`` if possible.

    Strings with suffixes ``B``, ``M``, or ``K`` are converted to their
    numeric equivalents.  Unparseable values are returned unchanged.
    """
    if isinstance(val, (int, float)):
        return val
    if val is None or val is pd.NA:
        return val
    if isinstance(val, str):
        s = val.strip().replace(",", "")
        multipliers = {
            "T": 1_000_000_000_000,
            "B": 1_000_000_000,
            "M": 1_000_000,
            "K": 1_000,
        }
        if s:
            last = s[-1].upper()
            mult = multipliers.get(last)
            if mult:
                try:
                    return float(s[:-1]) * mult
                except ValueError:
                    return val
        try:
            return float(s)
        except ValueError:
            return val
    return val
