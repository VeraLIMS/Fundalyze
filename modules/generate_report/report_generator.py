"""
script: report_generator.py

Dependencies:
    pip install openbb[all] matplotlib pandas

Usage:
    python src/report_generator.py AAPL MSFT GOOGL
"""

from __future__ import annotations

import os
import sys

from modules.generate_report import report_utils as rutils
from modules.generate_report.utils import iso_timestamp_utc

# Delay heavy OpenBB import until needed
obb = None


def _get_openbb():
    """Load OpenBB lazily and return the module."""
    global obb
    if obb is None:
        from openbb import obb as _obb
        obb = _obb
    return obb


def fetch_and_compile(
    symbol: str,
    base_output: str | None = None,
    *,
    price_period: str = "1mo",
    statements: list[str] | None = None,
    local_output: bool | None = None,
    write_json: bool = False,
) -> None:
    """Generate all report files for ``symbol``.

    Parameters
    ----------
    symbol:
        Ticker to process.
    base_output:
        Folder where ticker subdirectory will be created. Defaults to
        :func:`modules.config_utils.get_output_dir`.
    price_period:
        Price history duration passed to OpenBB/yfinance.
    statements:
        Iterable of statement types (``"income"``, ``"balance"``, ``"cash"``)
        to download. By default all three are fetched.
    write_json:
        When ``True`` also output JSON files in addition to CSV/PNG.
    """
    obb_mod = _get_openbb()

    if local_output is None:
        local_output = bool(base_output or os.getenv("OUTPUT_DIR")) or not bool(
            os.getenv("DIRECTUS_URL")
        )

        if base_output is not None or os.getenv("OUTPUT_DIR"):
            # Explicit output folder implies local writes even when Directus is configured
            local_output = True
        else:
            local_output = not bool(os.getenv("DIRECTUS_URL"))

    ticker_dir = rutils.ensure_output_dir(symbol, base_output) if local_output else (base_output or ".")
    metadata = {
        "ticker": symbol.upper(),
        "generated_on": iso_timestamp_utc(),
        "files": {},
    }

    lines: list[str] = [f"# Report for {symbol.upper()}", "*Generated via OpenBB Platform*", ""]

    rutils.fetch_profile(
        obb_mod,
        symbol,
        ticker_dir,
        metadata,
        lines,
        write_files=local_output,
        write_json=write_json,
    )
    lines.append("## 2) Price History (Last 1 Month)\n")
    rutils.fetch_price_history(
        obb_mod,
        symbol,
        ticker_dir,
        metadata,
        lines,
        price_period=price_period,
        write_files=local_output,
        write_json=write_json,
    )
    rutils.fetch_financial_statements(
        obb_mod,
        symbol,
        ticker_dir,
        metadata,
        lines,
        statements=statements,
        write_files=local_output,
        write_json=write_json,
    )
    if local_output:
        rutils.write_report_and_metadata(ticker_dir, lines, metadata)
        print(f"✅ Completed report for {symbol.upper()}: {os.path.join(ticker_dir, 'report.md')}")
    else:
        print(f"✅ Completed report for {symbol.upper()} (uploaded to Directus)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/report_generator.py <TICKER1> [TICKER2] [...]")
        sys.exit(1)

    for tick in sys.argv[1:]:
        fetch_and_compile(tick.strip())
