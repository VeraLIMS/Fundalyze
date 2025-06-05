# Core Enhancement Summary

## Updated Modules
- **modules/data/fetching.py** – `fetch_basic_stock_data_batch` now supports a
  `max_workers` parameter for optional parallel fetching.
- **modules/utils/data_utils.py** – added `read_json_if_exists` helper for safe
  JSON ingestion.

- **modules/utils/data_utils.py** – new helper module providing `strip_timezones`, `ensure_period_column`, and `read_csv_if_exists`.
- **modules/generate_report/excel_dashboard.py** – refactored to use the new utilities, reducing repetitive CSV loading logic and simplifying timezone handling.
- **modules/data/fetching.py** – added a `provider` parameter to `fetch_basic_stock_data` for explicit data source selection and improved error messages.
- **docs/API_REFERENCE.md** – updated to document the new function signature.
- **tests/test_fetching.py** – expanded test coverage for the new provider option.
- **modules/data/fetching.py** – added `fetch_basic_stock_data_batch` helper for multi-ticker retrieval.
- **modules/analytics/__init__.py** – new `moving_average` analysis helper.
- **modules/generate_report/report_generator.py** – accepts a `price_period` parameter for flexible price history.
- **tests/test_output_dir_env.py** – verifies custom period forwarding.
- **modules/generate_report/report_utils.py** – new helper module with reusable functions for profile, price and statement downloads.
- **modules/generate_report/report_generator.py** – refactored to use `report_utils` and now supports a `statements` parameter to choose which financial statements to fetch.
- **docs/API_REFERENCE.md** – signature updated again with the new `statements` option.
- **modules/generate_report/excel_dashboard.py** – further modularized with `_load_ticker_data`, `_assemble_tables` and `_write_dashboard` helpers.
- **modules/data/fetching.py** – `fetch_basic_stock_data_batch` now accepts `dedup` and `progress` parameters for convenience.
- **docs/API_REFERENCE.md** – description updated for the new batch options.
- **tests/test_fetching.py** – covers deduplication and progress output.

## Key Refactors

```python
# Old CSV loading in excel_dashboard.py
if ia_path.exists():
    df = pd.read_csv(ia_path, index_col=0)
    df = df.reset_index().rename(columns={"index": "Period"})
    income_ann[ticker] = _strip_timezones(df)
```

```python
# New approach using data_utils helpers
stmt_files = [
    ("income_annual.csv", income_ann),
    ...
]
for fname, storage in stmt_files:
    df = read_csv_if_exists(td / fname, index_col=0)
    if df is not None:
        df = ensure_period_column(df)
        storage[ticker] = strip_timezones(df)
```

## Added Feature

`fetch_basic_stock_data` now accepts a `provider` argument (`"yf"`, `"fmp"`, or `"auto"`) allowing callers to force a specific data source.

Additional helpers were introduced:

```python
df = fetch_basic_stock_data_batch(["AAPL", "MSFT"])
prices = moving_average(df_prices["Close"], window=20)
fetch_and_compile("AAPL", price_period="5d")
```


### 2024-Refactor Updates

- **modules/utils/excel_utils.py** – new utility with `col_to_letter` and `write_table` used for Excel dashboard creation.
- **modules/generate_report/excel_dashboard.py** – uses `write_table` to reduce nearly 80 lines of repeated code and now prints a simple progress indicator when reading ticker data.
- **modules/data/compare.py** – added missing `logging` import and file docstring.
- **tests/test_excel_dashboard.py** – updated to import the column helper from `modules.utils.excel_utils`.

```python
# Old repeated table-writing logic
worksheet.add_table(
    table_range,
    {
        "name": "PriceHistory_Table",
        "columns": [{"header": c} for c in df_prices.columns],
        "autofilter": True,
        "style": "Table Style Medium 3",
    },
)

# New helper usage
write_table(writer, df_prices, "PriceHistory", "PriceHistory_Table", style="Table Style Medium 3")
```

### 2025 Modular report generator

```python
# Old monolithic function
def fetch_and_compile(...):
    # hundreds of lines handling profile, prices and statements

# New approach
def fetch_and_compile(...):
    obb = _get_openbb()
    rutils.fetch_profile(...)
    rutils.fetch_price_history(...)
    rutils.fetch_financial_statements(...)
    rutils.write_report_and_metadata(...)
```

### 2025 Math utilities and fallback improvements

- **modules/utils/math_utils.py** – new helper module providing `moving_average` and `percentage_change`.
- **modules/analytics/__init__.py** – now re-exports these math helpers.
- **modules/generate_report/fallback_data.py** – implemented `fetch_1mo_prices_fmp` for FMP-based price retrieval.
- **modules/generate_report/excel_dashboard.py** – `_write_dashboard` simplified using a loop over table specs.
- **docs/overview.md** and **docs/API_REFERENCE.md** – updated to document the new math utilities.
- **tests** – added coverage for `percentage_change` and the FMP price fetch.

```python
from modules.utils.math_utils import percentage_change
s = pd.Series([1, 2, 4])
pct = percentage_change(s)
```

## 2026 Progress utilities and dashboard improvements

- **modules/utils/progress_utils.py** – new helper providing ``progress_iter`` for optional ``tqdm`` progress bars.
- **modules/data/fetching.py** – ``fetch_basic_stock_data_batch`` now uses ``progress_iter`` for sequential progress output.
- **modules/generate_report/excel_dashboard.py** – ``create_dashboard`` and ``create_and_open_dashboard`` accept a ``progress`` flag and use ``progress_iter`` when loading ticker data. ``_safe_concat_normal`` optimized via list comprehension.
- **tests** – added ``test_progress_utils.py`` and a progress variant of dashboard creation.

```python
from modules.utils.progress_utils import progress_iter
for item in progress_iter(items, description="work"):
    do_work(item)
```

### 2027 Updates
- **modules/data/fetching.py** – progress bar now works when using `ThreadPoolExecutor` and updated docstring.
- **modules/generate_report/report_generator.py** – default `local_output` logic respects custom `OUTPUT_DIR` or explicit `base_output`.
- **modules/generate_report/excel_dashboard.py** – `_transpose_financials` refactored for clarity; docstring expanded.
- **modules/management/portfolio_manager/portfolio_manager.py** – always writes local portfolio file even when Directus sync succeeds.

### 2028 JSON export option
- **modules/utils/data_utils.py** – added `write_dataframe` helper to save DataFrames as CSV and optional JSON.
- **modules/generate_report/report_utils.py** – profile, price history and statement functions accept `write_json` flag.
- **modules/generate_report/report_generator.py** – exposes `write_json` parameter forwarding to report utilities.
- **README.md** – updated example to demonstrate JSON export.

