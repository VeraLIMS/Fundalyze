# Developer Guide

This guide provides a high level look at Fundalyze's architecture and practical tips for extending or debugging the project.

## Architecture Overview

```
Fundalyze/
├── modules/          # Core packages
│   ├── analytics/    # Portfolio analysis helpers
│   ├── data/         # Data retrieval utilities
│   ├── generate_report/  # Report creation logic
│   ├── management/   # CLI tools for portfolio, groups and settings
│   └── utils/        # Small helper utilities
├── scripts/          # Entry points such as `main.py`
├── tests/            # Pytest suite
└── docs/             # Project documentation
```

* `modules/analytics` exposes functions like `portfolio_summary`.
* `modules/data` and `modules/config_utils` handle data fetching and configuration.
* `modules/generate_report` builds dashboards from downloaded CSV files.
* `modules/management` contains interactive CLI commands.

## Debugging Environment

1. Create the virtual environment with `bootstrap_env.sh` (or `.ps1` on Windows).
2. Open the repository in VS Code and start the **Python: Current File** debugger on `scripts/main.py`.
   Breakpoints inside `modules/` will be hit automatically.
3. Enable verbose logs by adding `LOG_LEVEL=DEBUG` to `config/.env`.
4. When debugging report generation you can set `OUTPUT_DIR` to a temporary folder to avoid clutter.

## Extending Fundalyze

### Adding Analysis Modules

1. Place a new `.py` file under `modules/analytics/` and implement your functions.
2. Re-export them in `modules/analytics/__init__.py` so other packages can import them.
3. Regenerate `docs/API_REFERENCE.md` by running `python -m pydoc` on the new module.

### Adding CLI Components or UI Elements

1. Add your implementation under `modules/management/`.
2. Register a menu entry in `scripts/main.py` so users can access it.
3. Document any new commands in the README or user guide.

## Writing Tests

- Tests live in the `tests/` directory and should be named `test_*.py`.
- Use `pytest -q` to run the suite. Aim to cover new code paths and keep coverage high.
- Fixtures for common setup reside in `tests/conftest.py`.
- Prefer temporary directories and small sample data to keep tests fast.
