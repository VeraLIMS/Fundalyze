# Fundalyze

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Build](https://img.shields.io/badge/build-manual-lightgrey)](#)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](#)

**Fundalyze** is an open source toolkit for fetching financial data, analysing investment portfolios and producing Excel dashboards. It uses OpenBB and yfinance with optional fallbacks to FMP, making it easy to track stocks and generate reports from the command line.

## Features

- Fetch company profiles, price history and financial statements
- Manage a portfolio and custom groups of stocks
- Automatically create Excel dashboards with charts
- Fallback data enrichment when primary sources fail

## Installation

### Clone the repository
```bash
git clone https://github.com/VeraLIMS/Fundalyze.git
cd Fundalyze
```

### Create a virtual environment

**Windows**
```powershell
.\bootstrap_env.ps1
```

**macOS/Linux**
```bash
./bootstrap_env.sh
```

Both scripts create `.venv`, activate it and install packages from `requirements.txt`.
If you prefer manual setup:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set environment variables such as API tokens inside `config/.env`:
```env
OPENBB_API_KEY=your-key
FMP_API_KEY=your-key
```

## Quickstart

1. Launch the CLI:
   ```bash
   python scripts/main.py
   ```
2. Choose **Generate Reports** and enter a few ticker symbols.
3. Open the generated Excel file under `output/` to view a dashboard of prices and fundamentals.

## Folder Structure

- `modules/` – core functionality and CLI helpers
- `scripts/` – entry points, including `main.py`
- `tests/` – pytest suite
- `docs/` – additional documentation

## More Information

- [Detailed Docs](docs/overview.md)
- [Developer Guide](docs/DEVELOPER_GUIDE.md)
- [Issue Tracker](https://github.com/VeraLIMS/Fundalyze/issues)

Fundalyze is licensed under the [Apache 2.0 License](LICENSE).
