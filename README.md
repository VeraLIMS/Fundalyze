# Fundalyze

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Build](https://img.shields.io/badge/build-manual-lightgrey)](#)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](#)

**Fundalyze** is a lightweight toolkit for fetching financial data, analysing portfolios and producing Excel dashboards. It leverages [OpenBB](https://openbb.co/) and `yfinance` with optional fallbacks to Financial Modeling Prep.

## Features

- Fetch company profiles, price history and statements
- Manage a local portfolio and custom groups
- Generate Excel dashboards with charts
- Fallback data enrichment when primary sources fail

## Installation

### 1. Clone and set up a virtual environment
```bash
git clone https://github.com/VeraLIMS/Fundalyze.git
cd Fundalyze
```

**Windows**
```powershell
./bootstrap_env.ps1
```

**macOS/Linux**
```bash
./bootstrap_env.sh
```
Both scripts create `.venv`, activate it and install Python packages from `requirements.txt`.

If you prefer manual setup:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment variables
Create `config/.env` with your API tokens:
```env
OPENBB_API_KEY=your-openbb-token
FMP_API_KEY=your-fmp-key
OUTPUT_DIR=output
```
See [docs/configuration.md](docs/configuration.md) for all options.

## Quickstart

1. Launch the CLI and select **Generate Reports**:
   ```bash
   python scripts/main.py report
   ```
2. Enter a list of tickers (e.g. `AAPL MSFT TSLA`).
3. Once complete, open the Excel file created in `output/` to view the dashboard.

## Folder Structure

- `modules/` - application modules and CLI helpers
- `scripts/` - entry points such as `main.py`
- `tests/` - pytest suite
- `docs/` - additional documentation

## Resources

- [Documentation](docs/overview.md)
- [Developer Guide](docs/DEVELOPER_GUIDE.md)
- [Issue Tracker](https://github.com/VeraLIMS/Fundalyze/issues)

Fundalyze is licensed under the [Apache 2.0 License](LICENSE).
