"""
script: report_generator.py

Dependencies:
    pip install openbb[all] matplotlib pandas

Usage:
    python src/report_generator.py AAPL MSFT GOOGL
"""

import os
import sys
import json
import pandas as pd
import matplotlib.pyplot as plt

from modules.config_utils import get_output_dir
from .utils import iso_timestamp_utc, record_file_metadata

# Delay heavy OpenBB import until needed
obb = None


def _ensure_openbb() -> None:
    """Lazily import :mod:`openbb` when first required."""
    global obb
    if obb is None:
        from openbb import obb as _obb
        obb = _obb


def _fetch_profile(symbol: str, ticker_dir: str, report_lines: list, metadata: dict) -> None:
    """Fetch company profile and update ``report_lines`` and ``metadata``."""
    _ensure_openbb()
    profile_path = os.path.join(ticker_dir, "profile.csv")
    fmp_profile_url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}"
    try:
        profile_obj = obb.equity.profile(symbol=symbol)
        profile_df = profile_obj.to_df()
        profile_df.to_csv(profile_path, index=False)
        report_lines.append("- → Saved full profile to `profile.csv`\n\n")
        report_lines.append(
            f"**Source:** OpenBB (`equity.profile`) — [FMP Company Profile]({fmp_profile_url})\n\n"
        )
        record_file_metadata(metadata, "profile.csv", "OpenBB (equity.profile)", fmp_profile_url)
    except Exception as e:
        report_lines.append(f"> Error fetching profile for {symbol}: {e}\n\n")
        report_lines.append("**Source:** ERROR occurred; see metadata.json\n\n")
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
        record_file_metadata(metadata, "profile.csv", f"ERROR: {e}", fmp_profile_url)


def _fetch_price_history(symbol: str, ticker_dir: str, report_lines: list, metadata: dict) -> None:
    """Fetch 1‑month price history and chart."""
    _ensure_openbb()
    price_csv_path = os.path.join(ticker_dir, "1mo_prices.csv")
    price_chart_path = os.path.join(ticker_dir, "1mo_close.png")
    yahoo_hist_url = f"https://finance.yahoo.com/quote/{symbol}/history?p={symbol}"
    try:
        hist_obj = obb.equity.price.historical(symbol=symbol, period="1mo", provider="yfinance")
        hist_df = hist_obj.to_df()
        for col in ("Dividends", "Stock Splits"):
            if col in hist_df.columns:
                hist_df = hist_df.drop(columns=[col])
        hist_df.to_csv(price_csv_path, index=False)
        report_lines.append("- → Saved 1 month price history to `1mo_prices.csv`\n\n")
        report_lines.append(
            f"**Source:** OpenBB (`equity.price.historical`, provider=`yfinance`) — [Yahoo Finance History]({yahoo_hist_url})\n\n"
        )
        plt.figure(figsize=(8, 4))
        hist_df["Close"].plot(title=f"{symbol} Close Price (Last 1 Month)")
        plt.xlabel("Date")
        plt.ylabel("Close Price (USD)")
        plt.tight_layout()
        plt.savefig(price_chart_path, dpi=150)
        plt.close()
        report_lines.append("- → Saved price chart to `1mo_close.png`\n\n")
        record_file_metadata(metadata, "1mo_close.png", "Visualization (matplotlib)")
        report_lines.append("Last 5 rows:\n\n")
        report_lines.append(hist_df.tail(5).to_markdown(tablefmt="github"))
        report_lines.append("\n\n")
        record_file_metadata(metadata, "1mo_prices.csv", "OpenBB (equity.price.historical, yfinance)", yahoo_hist_url)
    except Exception as e:
        report_lines.append(f"> Error fetching 1-month price history for {symbol}: {e}\n\n")
        report_lines.append("**Source:** ERROR occurred; see metadata.json\n\n")
        placeholder_cols = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
        pd.DataFrame(columns=placeholder_cols).to_csv(price_csv_path, index=False)
        record_file_metadata(metadata, "1mo_prices.csv", f"ERROR: {e}", yahoo_hist_url)


def _fetch_financials(symbol: str, ticker_dir: str, report_lines: list, metadata: dict) -> None:
    """Fetch financial statements via OpenBB."""
    _ensure_openbb()
    report_lines.append("## 3) Financial Statements\n")
    statements = [
        ("income", "Annual Income Statement", "annual", "income_annual.csv", f"https://finance.yahoo.com/quote/{symbol}/financials"),
        ("income", "Quarterly Income Statement", "quarter", "income_quarter.csv", f"https://finance.yahoo.com/quote/{symbol}/financials"),
        ("balance", "Annual Balance Sheet", "annual", "balance_annual.csv", f"https://finance.yahoo.com/quote/{symbol}/balance-sheet"),
        ("balance", "Quarterly Balance Sheet", "quarter", "balance_quarter.csv", f"https://finance.yahoo.com/quote/{symbol}/balance-sheet"),
        ("cash", "Annual Cash Flow", "annual", "cash_annual.csv", f"https://finance.yahoo.com/quote/{symbol}/cash-flow"),
        ("cash", "Quarterly Cash Flow", "quarter", "cash_quarter.csv", f"https://finance.yahoo.com/quote/{symbol}/cash-flow"),
    ]
    for stmt, label, period, filename, source_url in statements:
        report_lines.append(f"### {label} ({period.title()})\n")
        fin_path = os.path.join(ticker_dir, filename)
        try:
            fn = getattr(obb.equity.fundamental, stmt)
            fin_obj = fn(symbol=symbol, period=period)
            fin_df = fin_obj.to_df()
            if isinstance(fin_df, pd.DataFrame) and not fin_df.empty:
                fin_df.to_csv(fin_path, index=True)
                report_lines.append(f"- → Saved to `{filename}`\n\n")
                report_lines.append(
                    f"**Source:** OpenBB (`equity.fundamental.{stmt}`, {period}) — [Yahoo Finance]({source_url})\n\n"
                )
                report_lines.append("First 3 rows:\n\n")
                report_lines.append(fin_df.head(3).to_markdown(tablefmt="github"))
                report_lines.append("\n\n")
                record_file_metadata(metadata, filename, f"OpenBB (equity.fundamental.{stmt}, {period})", source_url)
            else:
                report_lines.append(f"> {label} not available or empty for {symbol}.\n\n")
                pd.DataFrame().to_csv(fin_path)
                record_file_metadata(metadata, filename, "Empty DataFrame (no data returned)", source_url)
        except Exception as e:
            report_lines.append(f"> {label} error for {symbol}: {e}\n\n")
            report_lines.append("**Source:** ERROR occurred; see metadata.json\n\n")
            pd.DataFrame().to_csv(fin_path)
            record_file_metadata(metadata, filename, f"ERROR: {e}", source_url)


def _write_outputs(ticker_dir: str, report_lines: list, metadata: dict) -> None:
    """Write ``report.md`` and ``metadata.json`` into ``ticker_dir``."""
    report_path = os.path.join(ticker_dir, "report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    record_file_metadata(metadata, "report.md", "Aggregated Markdown report (multiple sources)")
    meta_path = os.path.join(ticker_dir, "metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"✅ Completed report for {os.path.basename(ticker_dir)}: {report_path}")


def fetch_and_compile(symbol: str, base_output: str | None = None):
    """Generate all report files for ``symbol`` under ``output/``.

    Steps performed:
        1. Create ``output/<symbol>/`` if needed.
        2. Fetch company profile.
        3. Fetch 1‑month price history and chart.
        4. Fetch annual/quarterly financial statements.
        5. Write ``report.md`` and ``metadata.json`` summarizing sources.

    Parameters
    ----------
    symbol:
        Stock ticker symbol.
    base_output:
        Optional root directory; defaults to :func:`modules.config_utils.get_output_dir`.
    """
    if base_output is None:
        base_output = str(get_output_dir())

    symbol = symbol.upper()
    ticker_dir = os.path.join(base_output, symbol)
    os.makedirs(ticker_dir, exist_ok=True)

    # Initialize metadata
    metadata = {
        "ticker": symbol,
        "generated_on": iso_timestamp_utc(),
        "files": {}
    }

    report_lines = []
    report_lines.append(f"# Report for {symbol}\n")
    report_lines.append(f"*Generated via OpenBB Platform*\n\n")

    report_lines.append("## 1) Company Profile\n")
    _fetch_profile(symbol, ticker_dir, report_lines, metadata)

    report_lines.append("## 2) Price History (Last 1 Month)\n")
    _fetch_price_history(symbol, ticker_dir, report_lines, metadata)

    _fetch_financials(symbol, ticker_dir, report_lines, metadata)

    _write_outputs(ticker_dir, report_lines, metadata)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/report_generator.py <TICKER1> [TICKER2] [...]")
        sys.exit(1)

    for tick in sys.argv[1:]:
        fetch_and_compile(tick.strip())
