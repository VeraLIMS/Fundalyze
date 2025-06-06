from __future__ import annotations

"""Helper utilities for report generation."""

import json
import os
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import pandas as pd

from modules.config_utils import get_output_dir
from modules.data import insert_items, prepare_records
from modules.utils.data_utils import write_dataframe
from .utils import iso_timestamp_utc


def ensure_output_dir(symbol: str, base_output: str | None = None) -> str:
    """Return ticker directory path creating it if needed."""
    root = Path(base_output or get_output_dir())
    ticker_dir = root / symbol.upper()
    ticker_dir.mkdir(parents=True, exist_ok=True)
    return str(ticker_dir)


def upload_dataframe(df: pd.DataFrame, collection: str) -> None:
    """Insert DataFrame rows into a Directus collection if configured."""
    if (
        not os.getenv("DIRECTUS_URL")
        or not (
            os.getenv("DIRECTUS_API_TOKEN") or os.getenv("DIRECTUS_TOKEN")
        )
        or df.empty
    ):
        return
    records = prepare_records(collection, df.to_dict(orient="records"))
    try:
        insert_items(collection, records)
    except Exception as exc:  # pragma: no cover - network errors
        print(f"Warning uploading to Directus: {exc}")


def write_report_and_metadata(ticker_dir: str, lines: Iterable[str], metadata: dict) -> None:
    """Write Markdown report and metadata.json in ``ticker_dir``."""
    report_path = Path(ticker_dir) / "report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    metadata["files"]["report.md"] = {
        "source": "Aggregated Markdown report (multiple sources)",
        "source_url": "",
        "created_at": iso_timestamp_utc(),
    }

    with open(Path(ticker_dir) / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)


def fetch_profile(
    obb,
    symbol: str,
    ticker_dir: str,
    metadata: dict,
    lines: list[str],
    *,
    write_files: bool = True,
    write_json: bool = False,
) -> None:
    """Fetch company profile via OpenBB.

    Successful data is written to ``profile.csv`` and recorded in
    ``metadata.json``.  If the OpenBB call fails a placeholder CSV is written and
    the metadata entry is marked with ``ERROR`` so later stages (metadata
    checker and fallback) can attempt a repair.

    Parameters
    ----------
    obb:
        Loaded OpenBB module.
    symbol:
        Ticker symbol to fetch.
    ticker_dir:
        Folder where output files will be stored.
    metadata:
        Metadata dictionary updated with file info.
    lines:
        List of Markdown lines describing actions.
    write_files:
        When ``True`` save CSV/JSON files locally.
    write_json:
        Additionally write a JSON version alongside the CSV.
    """
    profile_path = Path(ticker_dir) / "profile.csv"
    fmp_profile_url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}"

    try:
        profile_df = obb.equity.profile(symbol=symbol).to_df()
        if write_files:
            write_dataframe(profile_df, profile_path, write_json=write_json)
        upload_dataframe(profile_df, os.getenv("DIRECTUS_COMPANIES_COLLECTION", "companies"))
        lines.append("- → Saved full profile to `profile.csv`\n\n")
        lines.append(
            f"**Source:** OpenBB (`equity.profile`) — [FMP Company Profile]({fmp_profile_url})\n\n"
        )
        metadata["files"]["profile.csv"] = {
            "source": "OpenBB (equity.profile)",
            "source_url": fmp_profile_url,
            "fetched_at": iso_timestamp_utc(),
        }
    except Exception as exc:
        lines.append(f"> Error fetching profile for {symbol}: {exc}\n\n")
        lines.append("**Source:** ERROR occurred; see metadata.json\n\n")
        cols = [
            "symbol",
            "price",
            "beta",
            "volAvg",
            "mktCap",
            "lastDiv",
            "range",
            "changes",
            "exchange",
            "industry",
            "website",
            "description",
            "ceo",
            "sector",
            "country",
            "fullTimeEmployees",
            "phone",
            "address",
            "city",
            "state",
            "zip",
            "dcfDiff",
            "dcf",
            "image",
        ]
        pd.DataFrame(columns=cols).to_csv(profile_path, index=False)
        metadata["files"]["profile.csv"] = {
            "source": f"ERROR: {exc}",
            "source_url": fmp_profile_url,
            "fetched_at": iso_timestamp_utc(),
        }
        # Later steps (metadata_checker, fallback_data) look for this ERROR
        # entry to decide whether a re-fetch is required.


def fetch_price_history(
    obb,
    symbol: str,
    ticker_dir: str,
    metadata: dict,
    lines: list[str],
    *,
    price_period: str = "1mo",
    write_files: bool = True,
    write_json: bool = False,
) -> None:
    """Fetch price history and chart using OpenBB/yfinance.

    A CSV file (``1mo_prices.csv``) and PNG chart (``1mo_close.png``) are
    created for successful downloads.  Metadata entries reference the data
    source and the chart is noted as being generated locally.  Errors result in
    empty placeholder files with ``ERROR`` marked in ``metadata.json`` so that
    the fallback process knows to try again.

    Parameters
    ----------
    obb:
        Loaded OpenBB module.
    symbol:
        Ticker symbol.
    ticker_dir:
        Directory to write output files.
    metadata:
        Metadata dictionary updated with file info.
    lines:
        Markdown lines describing actions.
    price_period:
        History duration passed to OpenBB/yfinance.
    write_files:
        When ``True`` save CSV/PNG output locally.
    write_json:
        Additionally write JSON alongside the CSV file.
    """
    ticker_path = Path(ticker_dir)
    price_csv_path = ticker_path / "1mo_prices.csv"
    price_chart_path = ticker_path / "1mo_close.png"
    yahoo_hist_url = f"https://finance.yahoo.com/quote/{symbol}/history?p={symbol}"

    try:
        hist_df = (
            obb.equity.price.historical(
                symbol=symbol, period=price_period, provider="yfinance"
            ).to_df()
        )
        for col in ("Dividends", "Stock Splits"):
            if col in hist_df.columns:
                hist_df = hist_df.drop(columns=[col])

        if write_files:
            write_dataframe(hist_df, price_csv_path, write_json=write_json)
        upload_dataframe(hist_df, os.getenv("DIRECTUS_PRICES_COLLECTION", "price_history"))
        msg = (
            "- → Saved 1 month price history to `1mo_prices.csv`\n\n"
            if price_period == "1mo"
            else f"- → Saved {price_period} price history to `1mo_prices.csv`\n\n"
        )
        lines.append(msg)
        lines.append(
            f"**Source:** OpenBB (`equity.price.historical`, provider=`yfinance`) — [Yahoo Finance History]({yahoo_hist_url})\n\n"
        )

        if write_files:
            plt.figure(figsize=(8, 4))
            hist_df["Close"].plot(title=f"{symbol} Close Price ({price_period})")
            plt.xlabel("Date")
            plt.ylabel("Close Price (USD)")
            plt.tight_layout()
            plt.savefig(price_chart_path, dpi=150)
            plt.close()

            lines.append("- → Saved price chart to `1mo_close.png`\n\n")
        metadata["files"]["1mo_close.png"] = {
            "source": "Visualization (matplotlib)",
            "source_url": "",
            "fetched_at": iso_timestamp_utc(),
        }

        lines.append("Last 5 rows:\n\n")
        lines.append(hist_df.tail(5).to_markdown(tablefmt="github"))
        lines.append("\n\n")

        metadata["files"]["1mo_prices.csv"] = {
            "source": "OpenBB (equity.price.historical, yfinance)",
            "source_url": yahoo_hist_url,
            "fetched_at": iso_timestamp_utc(),
        }
    except Exception as exc:
        lines.append(f"> Error fetching 1-month price history for {symbol}: {exc}\n\n")
        lines.append("**Source:** ERROR occurred; see metadata.json\n\n")
        placeholder_cols = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
        pd.DataFrame(columns=placeholder_cols).to_csv(price_csv_path, index=False)
        metadata["files"]["1mo_prices.csv"] = {
            "source": f"ERROR: {exc}",
            "source_url": yahoo_hist_url,
            "fetched_at": iso_timestamp_utc(),
        }
        # This ERROR flag tells metadata_checker to re-fetch price data later.


def fetch_financial_statements(
    obb,
    symbol: str,
    ticker_dir: str,
    metadata: dict,
    lines: list[str],
    *,
    statements: Iterable[str] | None = None,
    write_files: bool = True,
    write_json: bool = False,
) -> None:
    """Fetch income, balance and cash statements from OpenBB.

    Each statement is saved to a CSV file (and optional JSON) and logged in the
    ticker's ``metadata.json``.  Failures create empty placeholder files with an
    ``ERROR`` source entry so :mod:`metadata_checker` or :mod:`fallback_data` can
    attempt retrieval from alternate sources later.

    Parameters
    ----------
    obb:
        Loaded OpenBB module.
    symbol:
        Ticker symbol.
    ticker_dir:
        Directory for output files.
    metadata:
        Metadata dictionary updated with file info.
    lines:
        Markdown log lines.
    statements:
        Iterable of statement types to fetch.
    write_files:
        Save CSV files when ``True``.
    write_json:
        Additionally save JSON alongside CSV.
    """
    if statements is None:
        statements = ["income", "balance", "cash"]

    lines.append("## 3) Financial Statements\n")

    maps = [
        ("income", "Annual Income Statement", "annual", "income_annual.csv", f"https://finance.yahoo.com/quote/{symbol}/financials"),
        ("income", "Quarterly Income Statement", "quarter", "income_quarter.csv", f"https://finance.yahoo.com/quote/{symbol}/financials"),
        ("balance", "Annual Balance Sheet", "annual", "balance_annual.csv", f"https://finance.yahoo.com/quote/{symbol}/balance-sheet"),
        ("balance", "Quarterly Balance Sheet", "quarter", "balance_quarter.csv", f"https://finance.yahoo.com/quote/{symbol}/balance-sheet"),
        ("cash", "Annual Cash Flow", "annual", "cash_annual.csv", f"https://finance.yahoo.com/quote/{symbol}/cash-flow"),
        ("cash", "Quarterly Cash Flow", "quarter", "cash_quarter.csv", f"https://finance.yahoo.com/quote/{symbol}/cash-flow"),
    ]

    for stmt, label, period, filename, source_url in maps:
        if stmt not in statements:
            continue
        lines.append(f"### {label} ({period.title()})\n")
        fin_path = Path(ticker_dir) / filename
        try:
            fn = getattr(obb.equity.fundamental, stmt)
            fin_df = fn(symbol=symbol, period=period).to_df()
            if isinstance(fin_df, pd.DataFrame) and not fin_df.empty:
                if write_files:
                    write_dataframe(fin_df, fin_path, write_json=write_json)
                collection = f"{stmt}_statement" if stmt != "cash" else "cash_flow"
                upload_dataframe(fin_df.reset_index(), os.getenv(f"DIRECTUS_{collection.upper()}_COLLECTION", collection))
                lines.append(f"- → Saved to `{filename}`\n\n")
                lines.append(
                    f"**Source:** OpenBB (`equity.fundamental.{stmt}`, {period}) — [Yahoo Finance]({source_url})\n\n"
                )
                lines.append("First 3 rows:\n\n")
                lines.append(fin_df.head(3).to_markdown(tablefmt="github"))
                lines.append("\n\n")
                metadata["files"][filename] = {
                    "source": f"OpenBB (equity.fundamental.{stmt}, {period})",
                    "source_url": source_url,
                    "fetched_at": iso_timestamp_utc(),
                }
            else:
                lines.append(f"> {label} not available or empty for {symbol}.\n\n")
                metadata["files"][filename] = {
                    "source": "Empty DataFrame (no data returned)",
                    "source_url": source_url,
                    "fetched_at": iso_timestamp_utc(),
                }
                if write_files:
                    empty_df = pd.DataFrame()
                    write_dataframe(empty_df, fin_path, write_json=write_json)
        except Exception as exc:
            lines.append(f"> {label} error for {symbol}: {exc}\n\n")
            lines.append("**Source:** ERROR occurred; see metadata.json\n\n")
            if write_files:
                empty_df = pd.DataFrame()
                write_dataframe(empty_df, fin_path, write_json=write_json)
            metadata["files"][filename] = {
                "source": f"ERROR: {exc}",
                "source_url": source_url,
                "fetched_at": iso_timestamp_utc(),
            }
            # Metadata checker/fallback will revisit this ERROR entry.
