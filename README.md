# Fundalyze

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Build](https://img.shields.io/badge/build-manual-lightgrey)](#)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](#)

**Fundalyze** is a Python toolkit for downloading fundamental market data,
managing your portfolio and generating interactive Excel dashboards. It relies on
[OpenBB](https://openbb.co/) and `yfinance` with optional fallbacks to
Financial Modeling Prep.

## Features

- Fetch company profiles, price history and financial statements
- Maintain a local portfolio and groups spreadsheet
- Build Excel dashboards complete with charts
- Fallback to alternative data sources when needed

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
Both scripts create `.venv`, activate it and install dependencies from
`requirements.txt`.

Manual setup works as well:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
If JavaScript tooling is added later, install Node.js and run `npm install` in
its directory.

### 2. Configure environment variables
Create `config/.env` and add your API tokens:
```env
OPENBB_API_KEY=your-openbb-token
FMP_API_KEY=your-fmp-key
OUTPUT_DIR=output
```
See [docs/configuration.md](docs/configuration.md) for all available options.

## Quickstart

Launch the interactive menu:
```bash
python scripts/main.py
```
Generate a report directly:
```bash
python scripts/main.py report
```
Enter tickers like `AAPL MSFT` and an Excel dashboard will appear under
`output/`.

You can also work programmatically:
```python
from modules.generate_report import fetch_and_compile
from modules.generate_report import excel_dashboard

fetch_and_compile("AAPL")
excel_dashboard.create_and_open_dashboard(tickers=["AAPL"])
```
Open the workbook to explore profile information, price history and
statements.

## Directus Field Mapping

The script `scripts/sync_directus_fields.py` automatically fetches all collections
and fields from the connected Directus instance and merges them into
`directus_field_map.json`.

**Usage:**
1. Ensure `DIRECTUS_API_URL` and `DIRECTUS_TOKEN` (or Directus credentials) are
   configured in your environment.
2. Run:
```bash
python scripts/sync_directus_fields.py
```
3. You will be prompted to:
   - Map new fields to target names.
   - Confirm type changes.
   - Remove fields or collections deleted from Directus.

**`directus_field_map.json` Structure:**
```jsonc
{
  "collections": {
    "portfolio": {
      "fields": {
        "id": { "type": "integer", "mapped_to": "portfolio_id" },
        "ticker": { "type": "string", "mapped_to": "symbol" }
      }
    }
  }
}
```
After merging, any unmapped fields will have `"mapped_to": null` and you will be
prompted to set them before the script exits.

## Folder Structure

- `modules/` – source code packages
- `scripts/` – command line entry points
- `tests/` – pytest suite
- `docs/` – extended documentation

`output/` will contain generated CSVs and dashboards.

## Resources

- [User Documentation](docs/overview.md)
- [Developer Guide](docs/DEVELOPER_GUIDE.md)
- [Issue Tracker](https://github.com/VeraLIMS/Fundalyze/issues)
- Community chat (TBD)

Fundalyze is licensed under the [Apache 2.0 License](LICENSE).
