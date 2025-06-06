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

from modules.analytics import portfolio_summary, correlation_matrix


def parse_args() -> argparse.Namespace:
    """Return parsed CLI arguments."""
    parser = argparse.ArgumentParser(description="Profile Fundalyze utilities")
    parser.add_argument("--tickers", type=int, default=5, help="Number of synthetic tickers")
    parser.add_argument("--periods", type=int, default=24, help="Periods per ticker")
    parser.add_argument("--metrics", type=int, default=6, help="Metrics per period")
    return parser.parse_args()


def _sample_portfolio_df(num_tickers: int, rows: int, metrics: int) -> pd.DataFrame:
    """Return a synthetic portfolio DataFrame with numeric columns."""
    data = np.random.rand(rows, metrics)
    df = pd.DataFrame(data, columns=[f"M{i}" for i in range(metrics)])
    df.insert(0, "Ticker", [f"T{i % num_tickers}" for i in range(rows)])
    sectors = ["Tech", "Finance", "Health"]
    df.insert(1, "Sector", np.random.choice(sectors, size=rows))
    return df


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
    df = _sample_portfolio_df(args.tickers, args.periods, args.metrics)

    summary_time = profile_function(portfolio_summary, df)
    corr_time = profile_function(correlation_matrix, df)

    print(f"portfolio_summary: {summary_time:.4f}s")
    print(f"correlation_matrix: {corr_time:.4f}s")


def main() -> None:
    args = parse_args()
    run_profile(args)


if __name__ == "__main__":
    main()
