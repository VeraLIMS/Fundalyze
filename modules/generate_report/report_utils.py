from __future__ import annotations

"""Helper utilities for report generation."""

import json
import os
from typing import Iterable

import matplotlib.pyplot as plt
import pandas as pd

from modules.config_utils import get_output_dir
from modules.data import insert_items, prepare_records
from .utils import iso_timestamp_utc


def ensure_output_dir(symbol: str, base_output: str | None = None) -> str:
    """Return ticker directory path creating it if needed."""
    if base_output is None:
        base_output = str(get_output_dir())
    ticker_dir = os.path.join(base_output, symbol.upper())
    os.makedirs(ticker_dir, exist_ok=True)
    return ticker_dir


def upload_dataframe(df: pd.DataFrame, collection: str) -> None:
    """Insert DataFrame rows into a Directus collection if configured."""
    if not bool(os.getenv("DIRECTUS_URL")) or df.empty:
        return
    records = prepare_records(collection, df.to_dict(orient="records"))
    try:
        insert_items(collection, records)
    except Exception as exc:  # pragma: no cover - network errors
        print(f"Warning uploading to Directus: {exc}")


def write_report_and_metadata(ticker_dir: str, lines: Iterable[str], metadata: dict) -> None:
    """Write Markdown report and metadata.json in ``ticker_dir``."""
    report_path = os.path.join(ticker_dir, "report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    metadata["files"]["report.md"] = {
        "source": "Aggregated Markdown report (multiple sources)",
        "source_url": "",
        "created_at": iso_timestamp_utc(),
    }

    with open(os.path.join(ticker_dir, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)


def fetch_profile(
    obb,
    symbol: str,
    ticker_dir: str,
    metadata: dict,
    lines: list[str],
    *,
    write_files: bool = True,
) -> None:
    """Fetch company profile via OpenBB."""
    profile_path = os.path.join(ticker_dir, "profile.csv")
    fmp_profile_url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}"

    try:
        profile_df = obb.equity.profile(symbol=symbol).to_df()
        if write_files:
            profile_df.to_csv(profile_path, index=False)
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


def fetch_price_history(
    obb,
    symbol: str,
    ticker_dir: str,
    metadata: dict,
    lines: list[str],
    *,
    price_period: str = "1mo",
    write_files: bool = True,
) -> None:
    """Fetch price history and chart using OpenBB/yfinance."""
    price_csv_path = os.path.join(ticker_dir, "1mo_prices.csv")
    price_chart_path = os.path.join(ticker_dir, "1mo_close.png")
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
            hist_df.to_csv(price_csv_path, index=False)
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


def fetch_financial_statements(
    obb,
    symbol: str,
    ticker_dir: str,
    metadata: dict,
    lines: list[str],
    *,
    statements: Iterable[str] | None = None,
    write_files: bool = True,
) -> None:
    """Fetch income, balance and cash statements from OpenBB."""
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
        fin_path = os.path.join(ticker_dir, filename)
        try:
            fn = getattr(obb.equity.fundamental, stmt)
            fin_df = fn(symbol=symbol, period=period).to_df()
            if isinstance(fin_df, pd.DataFrame) and not fin_df.empty:
                if write_files:
                    fin_df.to_csv(fin_path, index=True)
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
                    pd.DataFrame().to_csv(fin_path)
        except Exception as exc:
            lines.append(f"> {label} error for {symbol}: {exc}\n\n")
            lines.append("**Source:** ERROR occurred; see metadata.json\n\n")
            if write_files:
                pd.DataFrame().to_csv(fin_path)
            metadata["files"][filename] = {
                "source": f"ERROR: {exc}",
                "source_url": source_url,
                "fetched_at": iso_timestamp_utc(),
            }
