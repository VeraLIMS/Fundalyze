# Developer Guide

This guide explains the internal structure of **Fundalyze** and how to contribute new modules or debugging tools.

## Architecture Overview

```
Fundalyze/
├── modules/          # Core functionality
│   ├── analytics/    # Portfolio analysis helpers
│   ├── data/         # Data retrieval utilities
│   ├── generate_report/  # Report creation logic
│   └── management/   # CLI tools for portfolio, groups and settings
├── scripts/          # Entry points such as `main.py`
├── tests/            # Pytest suite
└── docs/             # Project documentation
```

* `modules/analytics` provides small helper functions like `portfolio_summary` and `correlation_matrix`.
* `modules/data` contains raw data fetching utilities and the Directus client.
* `modules/generate_report` builds dashboard reports from fetched data.
* `modules/management` houses user facing CLI commands.

## Debugging Environment

1. Create a virtual environment using the provided scripts:
   ```bash
   ./bootstrap_env.sh
   ```
   or on Windows:
   ```powershell
   .\bootstrap_env.ps1
   ```

2. Open the repository in VS Code and start debugging `scripts/main.py`. You can set breakpoints anywhere inside the `modules` packages. Running the **Python: Current File** debugger automatically picks up the active virtual environment.

3. Enable verbose logging by setting environment variables in `config/.env`:
   ```env
   LOG_LEVEL=DEBUG
   ```
   The CLI then prints additional details useful during development.

## Extending Fundalyze

### New Analysis Modules

1. Add a new `.py` file under `modules/analytics/` implementing your analysis functions.
2. Expose the functions in `modules/analytics/__init__.py` so they can be imported elsewhere.
3. Add unit tests under `tests/` to cover the new functionality.

### New CLI Components

1. Place your implementation inside `modules/management/`.
2. Register the new command in `scripts/main.py` so it appears in the menu.
3. Update documentation if user facing behaviour changes.

## Writing Tests

Fundalyze uses `pytest`. Place tests in the `tests/` directory and name them `test_*.py`.
Run the full suite with:
```bash
pytest -q
```
Ensure your changes keep all tests passing and strive for good coverage when adding new code.

