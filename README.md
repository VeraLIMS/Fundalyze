# Fundalyze

Fundalyze is a lightweight Python application for fetching, analyzing and visualizing investment portfolio data. It automates:

- **Data Acquisition** – fetches data via OpenBB and yfinance, automatically falling back to FMP when needed.
- **Metadata Management** – verifies each ticker's completeness, re-fetches missing files and records source URLs.
- **Dashboard Generation** – aggregates raw CSVs into a multi-sheet Excel workbook so metrics can be inspected over time.

With modular scripts for report generation, fallback data enrichment and portfolio/group analysis, Fundalyze scales from a few tickers to many.

---

## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/VeraLIMS/Fundalyze.git
   cd Fundalyze
   ```
2. **Bootstrap your environment** – the included scripts create a virtual environment and install requirements.

   **Windows (PowerShell)**
   ```powershell
   .\bootstrap_env.ps1
   ```
   **macOS/Linux (Bash)**
   ```bash
   ./bootstrap_env.sh
   ```

   The scripts create `.venv`, activate it and install packages from `requirements.txt`. When finished you remain inside the activated environment. Launch the application with:
   ```bash
   python scripts/main.py
   ```

## Usage

After bootstrapping run `python scripts/main.py` to open the interactive menu. The CLI now uses **tabulate** for nicely formatted tables. From here you can:

- Manage Portfolio
- Manage Groups
- Generate Reports (performs metadata checks and creates an Excel dashboard)
- Exit

Choose **Generate Reports** to enter ticker symbols, fetch data and build the dashboard.

You can also launch individual tools directly:

```bash
# open the portfolio manager
python scripts/main.py portfolio

# manage groups
python scripts/main.py groups

# generate reports without entering the menu
python scripts/main.py report

# manage Markdown notes
python scripts/main.py notes

# run metadata checker only
python scripts/main.py metadata

# fetch missing data using fallback logic
python scripts/main.py fallback

# create an Excel dashboard from existing CSVs
python scripts/main.py dashboard
```

## Project Layout

- `config/` – configuration files including `finance_api.yaml`, `term_mapping.json`, `.env` and `settings.json`.
- `modules/` – reusable Python modules with helpers such as `sector_counts()` and `correlation_matrix()`.
- `scripts/` – entry-point scripts like `main.py`.

### Comparing OpenBB and yfinance data

Run `python -m data.compare <TICKER>` to fetch company profiles from both sources. Differences are shown so you can choose which dataset to keep.

### Using Directus as a Data Store

Set the following environment variables to read/write portfolio and group data to Directus instead of the local Excel files:
```bash
export DIRECTUS_URL="https://your-directus.example.com"
export DIRECTUS_TOKEN="<API token>"
# Optional collection names
export DIRECTUS_PORTFOLIO_COLLECTION="portfolio"
export DIRECTUS_GROUPS_COLLECTION="groups"
```
When these variables are present the tools will use Directus and automatically fall back to Excel if it is not reachable. You can configure these values interactively from the **Directus Connection** wizard inside the Settings Manager (`python scripts/main.py settings`).

You can manage collections interactively using the **Directus Wizard**:

```bash
python scripts/main.py directus
```
This helper lists collections, shows fields and allows you to create new fields or insert items from the command line.

### Note Manager

A simple Markdown note system lives in `notes/`. Launch it with either the
dedicated script or the new CLI subcommand:
```bash
# old behaviour
python scripts/note_cli.py

# via the main CLI
python scripts/main.py notes
```
Notes support Obsidian-style `[[wikilinks]]` for linking between files.
Use the **Notes Directory** wizard in the Settings Manager if you want to store notes elsewhere.

### Configuration & Secrets

Place API keys (Directus, OpenBB, OpenAI) in `config/.env` and preferences in `config/settings.json`. These files are ignored by Git and are loaded automatically using `python-dotenv`.

### End-to-End Tests

Automated end-to-end tests simulate common user workflows. See [docs/end_to_end_tests.md](docs/end_to_end_tests.md) for details.

### Performance Tests

The repository includes a small profiling utility to check the speed of key
data processing functions. Run it with:

```bash
python scripts/performance_profile.py
```

Results are summarized in [docs/performance_benchmarks.md](docs/performance_benchmarks.md).

## Further Documentation

- [Codebase Overview](docs/overview.md) – quick tour of modules and entry points.
- [Configuration Guide](docs/configuration.md) – setting up `.env` and `settings.json`.
- [Report Generation Guide](docs/report_generation.md) – how reporting files are created.

## License

Fundalyze is licensed under the [Apache License 2.0](LICENSE).
