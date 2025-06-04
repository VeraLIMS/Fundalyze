"""Simple performance profiling for Fundalyze utilities.

This script runs key functions with synthetic data and reports
execution times and profiling statistics. It is intended for
quick performance regression checks after refactoring.

Usage:
    python scripts/performance_profile.py
"""

from __future__ import annotations

import cProfile
import os
import pstats
import sys

import pandas as pd
import numpy as np

SCRIPT_DIR = os.path.dirname(__file__)
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from modules.generate_report.excel_dashboard import (
    _safe_concat_normal,
    _transpose_financials,
)


def _make_financial_df(periods: int, metrics: int) -> pd.DataFrame:
    dates = pd.date_range("2020-01-01", periods=periods, freq="ME")
    data = np.random.rand(periods, metrics)
    df = pd.DataFrame(data, columns=[f"M{i}" for i in range(metrics)])
    df.insert(0, "Period", dates)
    return df


def _sample_data(num_tickers: int = 5) -> dict[str, pd.DataFrame]:
    return {f"T{i}": _make_financial_df(24, 6) for i in range(num_tickers)}


def profile_function(func, *args, **kwargs) -> float:
    """Profile *func* and return the elapsed time."""
    prof = cProfile.Profile()
    prof.enable()
    func(*args, **kwargs)
    prof.disable()
    ps = pstats.Stats(prof)
    ps.stream = None
    ps.sort_stats("cumulative")
    ps.print_stats(5)
    return ps.total_tt


def run_profile():
    ticker_dfs = _sample_data()

    scn_time = profile_function(_safe_concat_normal, ticker_dfs)
    tf_time = profile_function(_transpose_financials, ticker_dfs)

    print(f"_safe_concat_normal: {scn_time:.4f}s")
    print(f"_transpose_financials: {tf_time:.4f}s")


if __name__ == "__main__":
    run_profile()
