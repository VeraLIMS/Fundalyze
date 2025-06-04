# Fundalyze

Fundalyze is a lightweight Python application for fetching, analyzing and visualizing investment portfolio data. It automates:

- **Data Acquisition** – fetches prices, company profiles and financial statements via OpenBB, yfinance and FMP.
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

After bootstrapping run `python scripts/main.py` to open the menu. From here you can:

- Manage Portfolio
- Manage Groups
- Generate Reports (performs metadata checks and creates an Excel dashboard)
- Exit

Choose **Generate Reports** to enter ticker symbols, fetch data and build the dashboard.

## Project Layout

- `config/` – configuration files including `finance_api.yaml`, `term_mapping.json`, `.env` and `settings.json`.
- `modules/` – reusable Python modules with helpers such as `sector_counts()`.
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
When these variables are present the tools will use Directus and automatically fall back to Excel if it is not reachable.

### Note Manager

A simple Markdown note system lives in `notes/`. Launch it with:
```bash
python scripts/note_cli.py
```
Notes support Obsidian-style `[[wikilinks]]` for linking between files.

### Configuration & Secrets

Place API keys (Directus, OpenBB, OpenAI) in `config/.env` and preferences in `config/settings.json`. These files are ignored by Git and are loaded automatically using `python-dotenv`.
