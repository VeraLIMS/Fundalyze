# Bug Audit Report

## Modified Files
- **bootstrap_env.py** – removed unnecessary f-strings when no placeholders were present.
- **modules/generate_report/fallback_data.py** – replaced constant f-string.
- **modules/generate_report/report_generator.py** – converted several constant f-strings to plain strings.
- **modules/generate_report/yf_fallback.py** – converted constant f-string to plain string.
- **modules/management/group_analysis/group_analysis.py** – removed unused imports.
- **modules/management/portfolio_manager/portfolio_manager.py** – removed unused imports.
- **modules/management/settings_manager/settings_manager.py** – removed unused config constants.
- **wizards/directus_setup.py & notes_dir.py** – removed unused os imports.
- **tests/test_diff.py** – added test for empty dictionaries.
- **tests/test_interactive_profile.py** – expanded test coverage for multiple branches.
- **tests/test_directus_client.py & test_excel_dashboard_extra.py** – removed unused imports.
- **modules/generate_report/__init__.py** – removed unused `run_metadata_checker` import.
- **tests/test_data_utils_edge.py** – added edge case tests for data utilities.

## Remaining Warnings
- `modules/management/directus_tools/__init__.py` re-exports a function causing an unused import warning. This is intentional and can be ignored.

