# Report Generation

This guide explains how Fundalyze builds ticker reports and what files are produced.

## Workflow

The report workflow is orchestrated by `run_generate_report()` in `modules.generate_report`.
It performs the following steps:

1. Prompt for ticker symbols.
2. Call `fetch_and_compile()` for each ticker to download profile data, price history and financial statements.  Data is saved under `output/<TICKER>/`.
3. Run `metadata_checker` to re-fetch any files that failed during the initial download.
4. Run `fallback_data` which attempts additional yfinance/FMP downloads if information is still missing.
5. Build an Excel dashboard using `excel_dashboard.create_and_open_dashboard()` and open it automatically.

## Output Files

Each ticker directory contains:

- `profile.csv` – company profile information.
- `1mo_prices.csv` – one month of daily prices.
- `income_annual.csv` and `income_quarter.csv` – income statements.
- `balance_annual.csv` and `balance_quarter.csv` – balance sheets.
- `cash_annual.csv` and `cash_quarter.csv` – cash-flow statements.
- `report.md` – markdown summary listing the data sources.
- `metadata.json` – metadata describing the source and fetch time for every file.

An Excel workbook named `dashboard_<TIMESTAMP>.xlsx` is created from these CSVs and placed in the `output` folder.

## Command Example

Run the full workflow from the CLI:

```bash
python scripts/main.py report
```

After completion the Excel dashboard opens so you can explore the results.

See [docs/end_to_end_tests.md](end_to_end_tests.md) for automated scenarios covering this process.
