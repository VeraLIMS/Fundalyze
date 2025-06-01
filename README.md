# Fundalyze

Fundalyze is a lightweight Python application for fetching, analyzing, and visualizing investment portfolio data. It automates:

Data Acquisition: pulls historical and real-time prices, company profiles, and financial statements (income, balance sheet, cash flow) via OpenBB, yfinance, and FMP.

Metadata Management: verifies each ticker’s report completeness, re-fetches missing files, and records source URLs/timestamps.

Dashboard Generation: aggregates every ticker’s raw CSVs into a single, multi-sheet Excel workbook—each sheet transposed and converted into a named Table—so you can quickly inspect metrics over time and write structured formulas.

With modular scripts for report generation, fallback data enrichment, and portfolio/group analysis, Fundalyze scales from a few tickers to many and lays the groundwork for future database or web-based extensions.

This repository includes a **bootstrap script** (`bootstrap_env.ps1` for Windows) that:

1. **Creates** a Python virtual environment in `./.venv/` (if it doesn’t already exist).  
2. **Activates** that venv in the current shell session.  
3. **Installs** all packages listed in `requirements.txt` into the newly created venv.

---

## Usage (Windows PowerShell)

1. Open PowerShell in the project root.  
2. Run:
   ```powershell
   .\bootstrap_env.ps1

If ./.venv/ is missing, it will be created.

The script will then activate the venv for you.

Finally, it installs everything from requirements.txt.

Once complete, you remain inside the activated venv. Simply run:

python src/main.py

to launch the application.

