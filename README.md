# Fundalyze

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Build](https://img.shields.io/badge/build-manual-lightgrey)](#)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](#)

## What is Fundalyze?
Fundalyze is an open source toolkit for retrieving market fundamentals and
storing them in [Directus](https://directus.io/). It wraps
[OpenBB](https://openbb.co/) and `yfinance` so you can quickly analyze
companies and manage a portfolio entirely through the Directus API.

## Features
- Download company profiles, historical prices and financial statements
- Manage your portfolio and ticker groups directly in Directus
- Automatic fallback from OpenBB to yfinance and FMP when data is missing

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
```
The token is used by `modules.utils.get_openbb()` to authenticate with the OpenBB Hub
whenever data is requested. See [docs/configuration.md](docs/configuration.md) for all options.

## Quick Start
Run the interactive menu:
```bash
python scripts/main.py
```
Manage your portfolio:
```bash
python scripts/main.py portfolio
```
Debug how a ticker is mapped before insertion:
```bash
python scripts/main.py map-record
```

Programmatic use:
```python
from modules.data.unified_fetcher import fetch_and_store

record = fetch_and_store("AAPL")
```
The returned dictionary contains normalized company data.

### Run with Docker
Build the image and launch the CLI inside a container:
```bash
docker build -t fundalyze .
docker run -it --rm -p 8501:8501 fundalyze
```
The container installs dependencies from `requirements.txt`, runs
`python scripts/main.py`, and exposes port **8501** for Streamlit apps
or other tools that may use it.

## Directus Field Mapping
`scripts/sync_directus_fields.py` syncs your Directus instance to `directus_field_map.json`.
1. Ensure `DIRECTUS_API_URL` and `DIRECTUS_TOKEN` are set.
2. Run `python scripts/sync_directus_fields.py` and follow the prompts.

## Folder Structure
- `modules/` – source packages
- `scripts/` – CLI entry points
- `tests/` – pytest suite
- `docs/` – extended documentation

## Contributor Onboarding
1. Fork the repository and clone your fork.
2. Run `./bootstrap_env.sh` (or `.ps1` on Windows) to create `.venv` and install dependencies.
3. Copy `config.yaml.example` to `config.yaml` and `config/.env` from the example, then add your tokens.
4. Run `python scripts/main.py -m onboarding` to launch the setup wizard.
5. Execute `pytest -q` to ensure everything works before making changes.
See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.


## Resources
- [User Documentation](docs/overview.md)
- [CLI Scripts](docs/scripts_overview.md)
- [Developer Guide](docs/DEVELOPER_GUIDE.md)
- [Utilities Overview](docs/utils_overview.md)
- [Issue Tracker](https://github.com/VeraLIMS/Fundalyze/issues)
- Community chat (coming soon)

Fundalyze is licensed under the [Apache 2.0 License](LICENSE).
