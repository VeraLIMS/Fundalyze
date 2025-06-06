# Test Suite Overview

This folder contains all automated tests for **Fundalyze**.  File names follow
`test_<component>.py` with optional `_extra` or `_edge` suffixes for additional
cases.  Tests are grouped by the package they exercise:

## Analytics
- `test_analysis.py` – analytics helper functions

## Configuration
- `test_config_utils.py` – settings and `.env` handling
- `test_output_dir_env.py` – environment variable overrides

## Data Utilities
- `test_fetching.py` – stock data retrieval helpers
- `test_directus_client.py` – Directus API wrapper
- `test_directus_mapper.py` – mapping of Directus schema
- `test_directus_mapper_extra.py` – extra mapping scenarios
- `test_data_utils_edge.py` – edge cases for CSV/JSON helpers
- `test_data_compare_extra.py` – additional compare logic
- `test_diff.py` – regression tests for `diff_dict`

## Management Tools
- `test_portfolio_manager.py` – portfolio CLI
- `test_group_analysis.py` – group management CLI
- `test_note_manager.py` – markdown note system
- `test_management_package.py` – package exports
- `test_directus_tools_init.py` – Directus wizard entry point

## Integration / End-to-End
- `test_interactive_profile.py` – user prompts for profile selection
- `test_sync_directus_fields.py` – sync Directus metadata
- `test_integration.py` – multiple modules together
- `test_e2e.py` – high level workflow

Extra test files (`*_extra.py`, `*_edge.py`) hold miscellaneous scenarios that
supplement the main tests without cluttering them.
