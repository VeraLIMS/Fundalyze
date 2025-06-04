# Fundalyze

Fundalyze is a lightweight Python application for fetching, analyzing, and visualizing investment portfolio data. It automates:

- **Data Acquisition**: pulls historical and real-time prices, company profiles, and financial statements (income, balance sheet, cash flow) via OpenBB, yfinance, and FMP.
- **Metadata Management**: verifies each ticker’s report completeness, re-fetches missing files, and records source URLs/timestamps.
- **Dashboard Generation**: aggregates every ticker’s raw CSVs into a single, multi-sheet Excel workbook—each sheet transposed and converted into a named Table—so you can quickly inspect metrics over time and write structured formulas.

With modular scripts for report generation, fallback data enrichment, and portfolio/group analysis, Fundalyze scales from a few tickers to many and lays the groundwork for future database or web-based extensions.

---

## Getting Started

1. **Clone the repository**  
   ```bash
   git clone https://github.com/VeraLIMS/Fundalyze.git
   cd Fundalyze
Bootstrap your environment
This repository includes a bootstrap script that will:

Create a Python virtual environment in ./.venv/ (if it doesn’t already exist).

Activate that venv in your current shell session.

Install all packages listed in requirements.txt into the newly created venv.

Windows PowerShell
powershell
Copy
Edit
.\bootstrap_env.ps1
If ./.venv/ is missing, it will be created.

The script will activate the venv for you.

Finally, it installs everything from requirements.txt.

Once complete, you remain inside the activated venv. Simply run:

powershell
Copy
Edit
python src/main.py
to launch the application.

macOS/Linux (Bash/Zsh)
bash
Copy
Edit
./bootstrap_env.sh
If ./.venv/ is missing, it will be created.

The script will activate the venv in the current shell.

Finally, it installs everything from requirements.txt.

Once complete, you remain inside the activated venv. Simply run:

bash
Copy
Edit
python src/main.py
to launch the application.

Usage
After bootstrapping (and activating the venv), launch the main menu:

bash
Copy
Edit
python src/main.py
You will see options to:

Manage Portfolio

Manage Groups


Generate Reports (with metadata check, fallback, & Excel dashboard)

Exit

Choose Generate Reports to:

Enter ticker symbols (comma-separated).

Automatically fetch profiles, price history, and financial statements.

Run a metadata check to re-fetch any missing data.

Generate a multi-sheet Excel dashboard (with transposed tables) for quick analysis.

### Comparing OpenBB and yfinance data

The command `python -m data_compare <TICKER>` fetches company profile
information from both OpenBB and yfinance. If both sources return data,
the differences of key fields are printed and you can choose which
dataset to keep. This helps verify data completeness and gives direct
links back to the original sources.

### Using Directus as a Data Store

If you have a Directus instance available you can store the portfolio and group
information there instead of using the local Excel files. Set the environment
variables below before running the application:

```bash
export DIRECTUS_URL="https://your-directus.example.com"  # base URL of your Directus API
export DIRECTUS_TOKEN="<API token>"                       # token with read/write permissions
# Optional: override the collection names
export DIRECTUS_PORTFOLIO_COLLECTION="portfolio"
export DIRECTUS_GROUPS_COLLECTION="groups"
```

When these variables are present `portfolio_manager` and `group_analysis` will
read from and write to the specified Directus collections. If Directus is not
reachable the tools automatically fall back to the Excel files.

