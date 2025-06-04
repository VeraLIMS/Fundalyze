# Fundalyze

Fundalyze is a Python toolkit for tracking investment portfolios. It automates fetching market data, checking for missing files and compiling an Excel dashboard with a single command. The project is designed around small reusable modules so it works just as well for a couple of tickers as it does for dozens.

## Features

- **Data acquisition** using OpenBB and yfinance with automatic fallbacks
- **Metadata checks** that verify downloaded files and re-fetch incomplete data
- **Excel dashboard** generation to visualize metrics over time
- **Interactive CLI** for managing your portfolio, groups, notes and settings

## Installation

Clone the repository and run one of the bootstrap scripts to create a virtual environment and install the required packages:

```bash
# Windows
./bootstrap_env.ps1

# macOS/Linux
./bootstrap_env.sh
```

The scripts create `.venv`, activate it and install everything from `requirements.txt`. Afterwards you remain in the activated environment.

## Configuration

API tokens and user preferences live in `config/`:

- `config/.env` holds secrets such as API keys
- `config/settings.json` stores extra options like currency and timezone

Both files are optional and ignored by Git. They are loaded automatically when the application starts.

## Usage

Start the interactive menu with:

```bash
python scripts/main.py
```

From here you can manage portfolios and groups, generate reports, launch the note manager or edit your settings. Each tool is also available as a direct subcommand. Examples:

```bash
python scripts/main.py portfolio   # open portfolio manager
python scripts/main.py groups      # manage groups
python scripts/main.py report      # generate reports and Excel dashboard
python scripts/main.py notes       # open the note manager
```

### Directus integration

If you wish to store portfolio and group data in Directus rather than local Excel files, set the following environment variables:

```bash
export DIRECTUS_URL="https://your-directus.example.com"
export DIRECTUS_TOKEN="<API token>"
export DIRECTUS_PORTFOLIO_COLLECTION="portfolio"   # optional
export DIRECTUS_GROUPS_COLLECTION="groups"         # optional
```

The tools will automatically fall back to the Excel files if Directus cannot be reached.

## Running tests

Fundalyze ships with a comprehensive test suite. Run it with:

```bash
pytest -q
```

The end-to-end scenarios exercised by these tests are documented in [docs/end_to_end_tests.md](docs/end_to_end_tests.md).

## Additional documentation

- [Codebase Overview](docs/overview.md)
- [Configuration Guide](docs/configuration.md)
- [Performance Benchmarks](docs/performance_benchmarks.md)

