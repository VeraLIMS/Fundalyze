# CLI Scripts

This page documents the command line entry points provided in the `scripts/` directory. Each file can be executed directly with `python scripts/<name>.py` and is also accessible via `python scripts/main.py` where applicable.

## Overview

```
Fundalyze/scripts
├── main.py               # interactive menu and subcommands
├── note_cli.py           # dedicated note manager launcher
├── performance_profile.py# micro benchmark helper
├── run_tests.py          # sequential pytest runner
├── connectivity_test.py  # ping Directus API
└── sync_directus_fields.py# synchronize field mapping
```

## main.py
The primary entry point. Running without arguments launches an interactive menu. You may also supply a subcommand such as `portfolio` to jump directly to a tool. A global `--no-openbb` flag disables OpenBB data fetching for troubleshooting.

**Menu map**

```
1. Portfolio & Groups  -> portfolio/group CLI
2. Notes               -> note manager
3. Directus Tools      -> Directus helpers
4. Settings            -> edit configuration
5. Utilities           -> test runner and profiler
6. Exit                -> quit
```

Additional subcommands are available without entering the menu:
`summary`, `view-portfolio` and `view-profiles`.

**Flow chart**

```
interactive_menu()
├─ run_portfolio_groups()
├─ run_note_manager()
├─ run_directus_wizard()
├─ run_settings_manager()
├─ run_utilities_menu()
└─ exit_program()
```

## note_cli.py
Legacy launcher for the note manager. Equivalent to running `main.py notes`.

## performance_profile.py
Profiles core data-processing functions using synthetic data. Useful for detecting performance regressions.

## run_tests.py
Discovers and runs each `test_*.py` file under `tests/` sequentially. Provides a single command to execute the entire pytest suite.

## connectivity_test.py
Loads configuration from `config/.env` and performs a `GET <DIRECTUS_URL>/server/health` request. The script prints the HTTP status and a snippet of the response. Failure to connect or any non-2xx status results in exit code `1`.

## sync_directus_fields.py
Compares collections and fields in your Directus instance against `directus_field_map.json`. New collections/fields are presented for confirmation and deleted entries can be removed. If any API request fails, the script aborts and your existing mapping file remains unchanged.

## mapping_diagnostic.py
Prints the expected → mapped field names for key collections and can optionally
insert a test record. Run `python scripts/main.py diag` for a full diagnostic or
use the `test-mapping` and `test-insert` subcommands directly from `main.py`.

## add_missing_mappings.py
Appends any new keys found in a JSON dataset to `directus_field_map.json`.
Run with a collection name and path to a JSON file containing one or more
records. This is also available via `python scripts/main.py add-missing`.

## mapping_validator.py
Checks a JSON dataset against `directus_field_map.json` and warns about missing or invalid field mappings. Optionally inserts the mapped records into Directus. Run with a collection name and path to a JSON file. Use `--insert` to perform the upload.
