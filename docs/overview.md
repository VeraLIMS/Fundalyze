# Codebase Overview

This document summarizes the major modules and entry points within **Fundalyze**. Use it as a quick reference when exploring or extending the project.

## Module Packages

### `modules.generate_report`
Utilities for building ticker reports and Excel dashboards.
- `report_generator.py` – fetches profile data, price history and financial statements via OpenBB, saving each dataset under `output/<TICKER>/`.
- `metadata_checker.py` – scans downloaded metadata for errors and attempts to re‑fetch missing information.
- `fallback_data.py` – performs a full yfinance fallback when primary sources fail.
- `excel_dashboard.py` – combines individual CSV files into a multi‑sheet Excel workbook.

The package exposes the convenience function `run_generate_report()` which orchestrates all of the above steps.

### `modules.management`
Tools for maintaining local data files:
- `portfolio_manager` – CLI for creating and editing `portfolio.xlsx`.
- `group_analysis` – manage related tickers in `groups.xlsx`.
- `note_manager` – simple Markdown note system supporting `[[wikilinks]]`.

Importing `modules.management` exposes convenience functions such as
`run_portfolio_manager()` and `run_group_analysis()` for launching each tool
directly.

### `modules.data`
Lower-level helpers used across the app:
- `fetching.py` – small wrappers around yfinance and HTTP calls.
- `directus_client.py` – optional Directus integration for remote storage.
- `term_mapper.py` – maps common financial terms to API field names and stores the mapping in `config/term_mapping.json`.

### `modules.config_utils`
Loads environment variables from `config/.env` and user settings from `config/settings.json`. Call `load_settings()` once during startup so other modules can access configuration values via `os.getenv()` or the returned dictionary.

## Script Entry Points

The `scripts/` directory contains small wrappers that import the modules above:
- `main.py` – interactive menu and command-line interface. From here you can launch portfolio management, group tools, report generation and the note manager.
- `note_cli.py` – legacy entry point equivalent to running `main.py notes`.
- `performance_profile.py` – micro-benchmark utility.

Running `python scripts/main.py` without arguments opens the interactive menu; see the README for command examples.
