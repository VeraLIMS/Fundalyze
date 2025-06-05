#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# Profile the performance of critical data processing functions using
# synthetic data. Helps catch regressions in execution time.
# ---------------------------------------------------------------------------
"""Simple performance profiling for Fundalyze utilities.

This script runs key functions with synthetic data and reports execution times
and profiling statistics. It is intended for quick performance regression
checks after refactoring.
"""

from __future__ import annotations

import argparse
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


def parse_args() -> argparse.Namespace:
    """Return parsed CLI arguments."""
    parser = argparse.ArgumentParser(description="Profile Fundalyze utilities")
    parser.add_argument("--tickers", type=int, default=5, help="Number of synthetic tickers")
    parser.add_argument("--periods", type=int, default=24, help="Periods per ticker")
    parser.add_argument("--metrics", type=int, default=6, help="Metrics per period")
    return parser.parse_args()


def _make_financial_df(periods: int, metrics: int) -> pd.DataFrame:
    """Return a dummy financial DataFrame with *periods* rows."""
    dates = pd.date_range("2020-01-01", periods=periods, freq="ME")
    data = np.random.rand(periods, metrics)
    df = pd.DataFrame(data, columns=[f"M{i}" for i in range(metrics)])
    df.insert(0, "Period", dates)
    return df


def _sample_data(num_tickers: int, periods: int, metrics: int) -> dict[str, pd.DataFrame]:
    """Return a mapping of ticker symbol to synthetic financial data."""
    return {f"T{i}": _make_financial_df(periods, metrics) for i in range(num_tickers)}


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


def run_profile(args: argparse.Namespace) -> None:
    ticker_dfs = _sample_data(args.tickers, args.periods, args.metrics)

    scn_time = profile_function(_safe_concat_normal, ticker_dfs)
    tf_time = profile_function(_transpose_financials, ticker_dfs)

    print(f"_safe_concat_normal: {scn_time:.4f}s")
    print(f"_transpose_financials: {tf_time:.4f}s")


def main() -> None:
    args = parse_args()
    run_profile(args)


if __name__ == "__main__":
    main()
