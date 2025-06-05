# Core Enhancement Summary

## Updated Modules

- **modules/utils/data_utils.py** – new helper module providing `strip_timezones`, `ensure_period_column`, and `read_csv_if_exists`.
- **modules/generate_report/excel_dashboard.py** – refactored to use the new utilities, reducing repetitive CSV loading logic and simplifying timezone handling.
- **modules/data/fetching.py** – added a `provider` parameter to `fetch_basic_stock_data` for explicit data source selection and improved error messages.
- **docs/API_REFERENCE.md** – updated to document the new function signature.
- **tests/test_fetching.py** – expanded test coverage for the new provider option.

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

