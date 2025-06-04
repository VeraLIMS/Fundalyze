"""
script: report_generator.py

Dependencies:
    pip install openbb[all] matplotlib pandas

Usage:
    python src/report_generator.py AAPL MSFT GOOGL
"""

import os
import sys
import time
import json
import pandas as pd
import matplotlib.pyplot as plt

from modules.config_utils import get_output_dir

# Delay heavy OpenBB import until needed
obb = None


def fetch_and_compile(symbol: str, base_output: str | None = None):
    """
    1) Create output/<symbol>/
    2) Fetch company profile, save as profile.csv, record source & source_url
    3) Fetch 1mo prices, save 1mo_prices.csv & 1mo_close.png, record sources/URLs
    4) Fetch income/balance/cash (annual & quarterly), save CSVs, record sources/URLs
    5) Write report.md with clickable [label](url) for each source
    6) Write metadata.json containing {"source", "source_url", "fetched_at"} for each file
    """
    global obb
    if obb is None:
        from openbb import obb as _obb
        obb = _obb

    if base_output is None:
        base_output = str(get_output_dir())

    symbol = symbol.upper()
    ticker_dir = os.path.join(base_output, symbol)
    os.makedirs(ticker_dir, exist_ok=True)

    # Initialize metadata
    metadata = {
        "ticker": symbol,
        "generated_on": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "files": {}
    }

    report_lines = []
    report_lines.append(f"# Report for {symbol}\n")
    report_lines.append(f"*Generated via OpenBB Platform*\n\n")

    #
    # 1) Company Profile
    #
    report_lines.append("## 1) Company Profile\n")

    # Define profile_path before try/except
    profile_path = os.path.join(ticker_dir, "profile.csv")
    fmp_profile_url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}"

    try:
        profile_obj = obb.equity.profile(symbol=symbol)
        profile_df = profile_obj.to_df()
        profile_df.to_csv(profile_path, index=False)

        report_lines.append(f"- → Saved full profile to `profile.csv`\n\n")
        report_lines.append(f"**Source:** OpenBB (`equity.profile`) — [FMP Company Profile]({fmp_profile_url})\n\n")

        metadata["files"]["profile.csv"] = {
            "source": "OpenBB (equity.profile)",
            "source_url": fmp_profile_url,
            "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

    except Exception as e:
        report_lines.append(f"> Error fetching profile for {symbol}: {e}\n\n")
        report_lines.append("**Source:** ERROR occurred; see metadata.json\n\n")

        # Write an empty placeholder with expected columns
        cols = [
            "symbol", "price", "beta", "volAvg", "mktCap", "lastDiv", "range", "changes",
            "exchange", "industry", "website", "description", "ceo", "sector", "country",
            "fullTimeEmployees", "phone", "address", "city", "state", "zip", "dcfDiff",
            "dcf", "image"
        ]
        pd.DataFrame(columns=cols).to_csv(profile_path, index=False)

        metadata["files"]["profile.csv"] = {
            "source": f"ERROR: {e}",
            "source_url": fmp_profile_url,
            "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

    #
    # 2) Price History (Last 1 Month)
    #
    report_lines.append("## 2) Price History (Last 1 Month)\n")

    # Define paths and URL before try/except
    price_csv_path = os.path.join(ticker_dir, "1mo_prices.csv")
    price_chart_path = os.path.join(ticker_dir, "1mo_close.png")
    yahoo_hist_url = f"https://finance.yahoo.com/quote/{symbol}/history?p={symbol}"

    try:
        hist_obj = obb.equity.price.historical(
            symbol=symbol, period="1mo", provider="yfinance"
        )
        hist_df = hist_obj.to_df()
        for col in ("Dividends", "Stock Splits"):
            if col in hist_df.columns:
                hist_df = hist_df.drop(columns=[col])

        hist_df.to_csv(price_csv_path, index=False)
        report_lines.append(f"- → Saved 1 month price history to `1mo_prices.csv`\n\n")
        report_lines.append(f"**Source:** OpenBB (`equity.price.historical`, provider=`yfinance`) — [Yahoo Finance History]({yahoo_hist_url})\n\n")

        # Plot closing price
        plt.figure(figsize=(8, 4))
        hist_df["Close"].plot(title=f"{symbol} Close Price (Last 1 Month)")
        plt.xlabel("Date")
        plt.ylabel("Close Price (USD)")
        plt.tight_layout()
        plt.savefig(price_chart_path, dpi=150)
        plt.close()

        report_lines.append(f"- → Saved price chart to `1mo_close.png`\n\n")
        metadata["files"]["1mo_close.png"] = {
            "source": "Visualization (matplotlib)",
            "source_url": "",
            "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

        report_lines.append("Last 5 rows:\n\n")
        report_lines.append(hist_df.tail(5).to_markdown(tablefmt="github"))
        report_lines.append("\n\n")

        metadata["files"]["1mo_prices.csv"] = {
            "source": "OpenBB (equity.price.historical, yfinance)",
            "source_url": yahoo_hist_url,
            "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

    except Exception as e:
        report_lines.append(f"> Error fetching 1-month price history for {symbol}: {e}\n\n")
        report_lines.append("**Source:** ERROR occurred; see metadata.json\n\n")

        # Write placeholder CSV with standard columns
        placeholder_cols = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
        pd.DataFrame(columns=placeholder_cols).to_csv(price_csv_path, index=False)

        metadata["files"]["1mo_prices.csv"] = {
            "source": f"ERROR: {e}",
            "source_url": yahoo_hist_url,
            "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

    #
    # 3) Financial Statements (Annual + Quarterly for Income, Balance, Cash)
    #
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

        # Define CSV path outside of try/except
        fin_path = os.path.join(ticker_dir, filename)

        try:
            fn = getattr(obb.equity.fundamental, stmt)
            fin_obj = fn(symbol=symbol, period=period)
            fin_df = fin_obj.to_df()

            if isinstance(fin_df, pd.DataFrame) and not fin_df.empty:
                fin_df.to_csv(fin_path, index=True)
                report_lines.append(f"- → Saved to `{filename}`\n\n")
                report_lines.append(f"**Source:** OpenBB (`equity.fundamental.{stmt}`, {period}) — [Yahoo Finance]({source_url})\n\n")
                report_lines.append("First 3 rows:\n\n")
                report_lines.append(fin_df.head(3).to_markdown(tablefmt="github"))
                report_lines.append("\n\n")

                metadata["files"][filename] = {
                    "source": f"OpenBB (equity.fundamental.{stmt}, {period})",
                    "source_url": source_url,
                    "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                }

            else:
                report_lines.append(f"> {label} not available or empty for {symbol}.\n\n")
                metadata["files"][filename] = {
                    "source": "Empty DataFrame (no data returned)",
                    "source_url": source_url,
                    "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                }

                # Write an empty placeholder so downstream code sees a valid file
                pd.DataFrame().to_csv(fin_path)

        except Exception as e:
            report_lines.append(f"> {label} error for {symbol}: {e}\n\n")
            report_lines.append("**Source:** ERROR occurred; see metadata.json\n\n")

            # Write an empty placeholder
            pd.DataFrame().to_csv(fin_path)

            metadata["files"][filename] = {
                "source": f"ERROR: {e}",
                "source_url": source_url,
                "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }

    #
    # 4) Write the aggregated Markdown report
    #
    report_path = os.path.join(ticker_dir, "report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    metadata["files"]["report.md"] = {
        "source": "Aggregated Markdown report (multiple sources)",
        "source_url": "",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

    #
    # 5) Dump metadata.json
    #
    with open(os.path.join(ticker_dir, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"✅ Completed report for {symbol}: {report_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/report_generator.py <TICKER1> [TICKER2] [...]")
        sys.exit(1)

    for tick in sys.argv[1:]:
        fetch_and_compile(tick.strip())
