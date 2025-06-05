# Agent Instructions

This repository contains the Fundalyze Python application. The directory layout:

- `modules/` – core packages with data fetching utilities and portfolio management.
- `scripts/` – entry points including `main.py` for the CLI.
- `tests/` – pytest suite that covers core functionality.

## Expected Behavior

When modifying or adding any Python code or documentation, run the test suite:

```bash
pytest -q
```

All tests should pass before committing changes.

Provide concise commit messages and include PR summaries referencing relevant lines when describing changes.



## Recent Findings

```
........................................................................ [ 71%]
.............................                                            [100%]
101 passed in 4.93s
```


## Recent Findings

```
........................................................................ [ 67%]
..................................                                       [100%]
106 passed in 2.56s
```

## Recent Findings

```
........................................................................ [ 63%]
..........................................                               [100%]
=============================== warnings summary ===============================
tests/test_portfolio_manager.py::test_add_new_ticker_with_nas_present
tests/test_portfolio_manager.py::test_add_ticker_to_all_na_column
  /workspace/Fundalyze/modules/management/portfolio_manager/portfolio_manager.py:266: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
    portfolio = pd.concat([portfolio, new_row], ignore_index=True)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
114 passed, 2 warnings in 3.47s
```

## Recent Findings

```
........................................................................ [ 63%]
..........................................                               [100%]
=============================== warnings summary ===============================
tests/test_portfolio_manager.py::test_add_new_ticker_with_nas_present
tests/test_portfolio_manager.py::test_add_ticker_to_all_na_column
  /workspace/Fundalyze/modules/management/portfolio_manager/portfolio_manager.py:266: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
    portfolio = pd.concat([portfolio, new_row], ignore_index=True)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
114 passed, 2 warnings in 3.14s
```
