## Fix for "NA boolean ambiguous" in portfolio_manager

**Original Error Traceback:** when adding a ticker, the interactive menu crashed with:
```
TypeError: boolean value of NA is ambiguous
```
originating from `portfolio_manager.py` line 198.

**Before:** membership checks used raw `.values` which may contain `pd.NA`:
```python
if tk in portfolio["Ticker"].values:
```

**After:** drop `NA` values before membership tests via helper `ticker_exists`:
```python
existing = df["Ticker"].dropna().astype(str).values
return tk in existing
```
Calls were updated to use `ticker_exists(...)`.

**Files Modified**
- `modules/management/portfolio_manager/portfolio_manager.py`
- `modules/management/group_analysis/group_analysis.py`
- `tests/test_portfolio_manager.py`
- `REPORT_FIX_TICKER_NA.md`

**New Tests Added**
- `test_existing_ticker_with_na_skips_adding` – ensures duplicate tickers are skipped even with `pd.NA` present.
- `test_add_new_ticker_with_nas_present` – verifies adding a new ticker when existing column has NAs.
- `test_add_ticker_to_all_na_column` – verifies adding when column is entirely `NA`.
