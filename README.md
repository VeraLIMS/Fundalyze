# Fundalyze

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Build](https://img.shields.io/badge/build-manual-lightgrey)](#)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](#)

**Fundalyze** is a small Python toolkit for downloading fundamental data, analysing your stock portfolio and exporting Excel dashboards. It builds on [OpenBB](https://openbb.co/) and `yfinance` with optional fallbacks to Financial Modeling Prep.

## Features

- Fetch company profiles, price history and financial statements
- Manage a local portfolio and custom groups
- Create Excel dashboards complete with charts
- Optional fallback downloads when primary sources fail

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
Both scripts create `.venv`, activate it and install requirements from `requirements.txt`.

Manual setup works as well:
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
See [docs/configuration.md](docs/configuration.md) for all available settings.

## Quickstart

Generate a report from the command line:
```bash
python scripts/main.py report
```
Enter one or more tickers (e.g. `AAPL MSFT`) and an Excel dashboard appears in the `output/` folder.

You can also call the modules directly:
```python
from modules.generate_report import fetch_and_compile
from modules.generate_report import excel_dashboard

fetch_and_compile("AAPL")
excel_dashboard.create_and_open_dashboard(tickers=["AAPL"])
```

## Folder Structure

- `modules/` – source code packages
- `scripts/` – entry points including `main.py`
- `tests/` – pytest suite
- `docs/` – extended documentation

## Resources

- [User Documentation](docs/overview.md)
- [Developer Guide](docs/DEVELOPER_GUIDE.md)
- [Issue Tracker](https://github.com/VeraLIMS/Fundalyze/issues)

Fundalyze is licensed under the [Apache 2.0 License](LICENSE).
