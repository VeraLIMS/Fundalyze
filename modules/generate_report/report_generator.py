"""Utility for creating markdown reports from market data.

``report_generator.py`` coordinates OpenBB calls to fetch a company's profile,
price history and financial statements.  Each dataset is written to ``CSV`` and
optionally ``JSON``.  The function then compiles a markdown summary and a
``metadata.json`` file describing the source of every output.  The goal is to
produce a self‑contained folder under ``output/<TICKER>/`` that can later be
checked by :mod:`metadata_checker` and included in the Excel dashboard.

Dependencies
------------
``pip install openbb[all] matplotlib pandas``

Example
-------
``python src/report_generator.py AAPL MSFT GOOGL``
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

    The function orchestrates every step required to populate a ticker folder.
    It calls helper functions from :mod:`report_utils` to fetch the profile,
    price history and financial statements.  Markdown lines describing each
    action are accumulated in ``lines`` and finally written to ``report.md``.
    ``metadata.json`` is updated in parallel with details about the data source
    or, if an error occurs, an ``ERROR`` entry which later triggers the
    fallback utilities.

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
 codex/document-utilities-in-analytics-module
        # If a base_output path was provided, assume the caller expects local
        # files regardless of DIRECTUS_URL. Otherwise default to uploading when
        # DIRECTUS_URL is configured.
=======
 codex/document-scripts-folder-and-add-headers
        # If a base_output path was provided, assume the caller expects local
        # files regardless of DIRECTUS_URL. Otherwise default to uploading when
        # DIRECTUS_URL is not configured.
=======
 codex/document-logging_utils.py-usage
 codex/document-logging_utils.py-usage

=======
 codex/document-logs-and-logging-policy
        # If a ``base_output`` path was provided, assume the caller expects
        # local files regardless of DIRECTUS_URL. Otherwise default to uploading
        # when DIRECTUS_URL is configured.
=======
 codex/create-documentation-for-generate_report-module
=======
 nwk644-codex/document-utilities-in-analytics-module
 main
        # If a base_output path was provided, assume the caller expects local
        # files regardless of DIRECTUS_URL. Otherwise default to uploading when
        # DIRECTUS_URL is configured.
 main
 main
 main
 main
        local_output = bool(base_output or os.getenv("OUTPUT_DIR")) or not bool(
            os.getenv("DIRECTUS_URL")
        )
=======
 codex/document-config-folder-files
        # If a base_output path was provided, assume the caller expects local
        # files regardless of DIRECTUS_URL. Otherwise default to uploading when
        # DIRECTUS_URL is configured.
        local_output = bool(base_output or os.getenv("OUTPUT_DIR")) or not bool(os.getenv("DIRECTUS_URL"))
 main

 codex/document-scripts-folder-and-add-headers
=======
        if base_output is not None or os.getenv("OUTPUT_DIR"):
            # Explicit output folder implies local writes even when Directus is
            # configured
=======
        # Write locally when a specific output folder is provided or when no
        # Directus URL is configured. Otherwise default to uploading to
        # Directus.
        if base_output is not None or os.getenv("OUTPUT_DIR"):
 main
            local_output = True
        else:
            local_output = not bool(os.getenv("DIRECTUS_URL"))

 main
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
