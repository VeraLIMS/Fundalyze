# Developer Guide

This document outlines Fundalyze's architecture and provides tips for extending and debugging the project.

## Architecture Overview
```text
Fundalyze/
├── modules/            # Core packages
│   ├── analytics/      # Portfolio analysis helpers
│   ├── data/           # Data retrieval utilities
│   ├── generate_report/# Report creation logic
│   ├── management/     # CLI tools and menus
│   └── utils/          # Small helpers
├── scripts/            # Entry points such as `main.py`
├── tests/              # Pytest suite
└── docs/               # Documentation
```
- `modules/analytics` exposes functions like `portfolio_summary`.
- `modules/data` and `modules/config_utils` manage data fetching and settings.
- `modules/generate_report` builds Excel dashboards from downloaded CSVs.
- `modules/management` contains interactive CLI commands.

## Debugging Environment
1. Create the virtual environment with `bootstrap_env.sh` (or `.ps1` on Windows).
2. Open the project in VS Code and choose **Run → Start Debugging** on `scripts/main.py` to attach the debugger.
3. Set `LOG_LEVEL=DEBUG` in `config/.env` for verbose output.
4. Optionally set `OUTPUT_DIR` to a temporary folder when testing report generation.
5. For quick inspection you can run modules with:
   ```bash
   python -m pdb modules/<package>/file.py
   ```
6. Configure breakpoints in VS Code via `.vscode/launch.json` if you need custom args.

## Extending Fundalyze
### Adding Analysis Modules
1. Drop a `.py` file into `modules/analytics/` and implement your functions.
2. Register the module in `modules/analytics/__init__.py` (this acts as the simple *analysis registry*).
3. Regenerate `docs/API_REFERENCE.md` with `pydoc` on the new module.

### Adding CLI Components or UI Elements
1. Place new code under `modules/management/`.
2. Register a menu entry in `scripts/main.py` for access through the CLI.
3. Document any new commands in the README or user guide.
4. Reusable widgets belong in `modules/interface.py`.

## Writing Tests
- Tests live in `tests/` and use the `pytest` framework.
- Name files `test_*.py` and keep fixtures focused.
- Run `pytest -q` before committing to ensure coverage stays high.
- Prefer small sample data and temporary directories to keep tests fast.
