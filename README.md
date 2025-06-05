# Fundalyze

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Build](https://img.shields.io/badge/build-manual-lightgrey)](#)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](#)

## What is Fundalyze?
Fundalyze is an open source toolkit for retrieving market fundamentals and
building Excel dashboards. It wraps [OpenBB](https://openbb.co/) and
`yfinance` so you can quickly analyze companies and maintain a local
portfolio.

## Features
- Download company profiles, historical prices and financial statements
- Maintain a spreadsheet-based portfolio and groups list
- Generate Excel dashboards with charts
- Fallback to alternate data sources when needed

## Installation

### 1. Clone and create a virtual environment
```bash
git clone https://github.com/VeraLIMS/Fundalyze.git
cd Fundalyze
```
**Windows**
```powershell
./bootstrap_env.ps1
```
**macOS / Linux**
```bash
./bootstrap_env.sh
```
Both scripts create `.venv`, activate it and install dependencies from `requirements.txt`.
Manual setup works too:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Install Node.js and run `npm install` if JavaScript tools are added later.

### 2. Configure environment variables
Create `config/.env` and add your API tokens:
```env
OPENBB_TOKEN=your-openbb-token
FMP_API_KEY=your-fmp-key
OUTPUT_DIR=output
```
The token is used by `modules.utils.get_openbb()` to authenticate with the OpenBB Hub
whenever data is requested. See [docs/configuration.md](docs/configuration.md) for all options.

## Quickstart
Run the interactive menu:
```bash
python scripts/main.py
```
Generate a report directly:
```bash
python scripts/main.py report
```
Enter tickers such as `AAPL MSFT` and a dashboard will appear in `output/`.

Programmatic use:
```python
from modules.generate_report import fetch_and_compile, excel_dashboard

fetch_and_compile("AAPL", write_json=True)
excel_dashboard.create_and_open_dashboard(tickers=["AAPL"])
```
Open the workbook to explore profile information, prices and statements.

## Directus Field Mapping
`scripts/sync_directus_fields.py` syncs your Directus instance to `directus_field_map.json`.
1. Ensure `DIRECTUS_API_URL` and `DIRECTUS_TOKEN` are set.
2. Run `python scripts/sync_directus_fields.py` and follow the prompts.

## Folder Structure
- `modules/` – source packages
- `scripts/` – CLI entry points
- `tests/` – pytest suite
- `docs/` – extended documentation

`output/` holds generated CSVs and dashboards.

## Resources
- [User Documentation](docs/overview.md)
- [CLI Scripts](docs/scripts_overview.md)
- [Developer Guide](docs/DEVELOPER_GUIDE.md)
- [Utilities Overview](docs/utils_overview.md)
- [Issue Tracker](https://github.com/VeraLIMS/Fundalyze/issues)
- Community chat (coming soon)

Fundalyze is licensed under the [Apache 2.0 License](LICENSE).
