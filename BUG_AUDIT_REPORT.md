# Bug Audit Report

## Modified Files
- **modules/data/term_mapper.py** – Updated OpenAI integration to use the v1 client interface.
- **modules/generate_report/excel_dashboard.py** – Guarded `os.startfile` usage for non-Windows platforms and silenced linter false positive.
- **tests/test_term_mapper_extra.py** – Added new tests for `_suggest_with_openai` covering missing API key and missing module cases.
- **modules/management/directus_tools/__init__.py** – Added public export list and module docstring.
- **modules/generate_report/excel_dashboard.py** – Removed duplicate imports flagged by static analysis.
- **tests/test_term_mapper_extra.py** – Dropped unused `os` import.
- **tests/test_directus_tools_init.py** – New tests verifying `run_directus_wizard` export.
- **modules/utils/excel_utils.py** – Added validation for negative indices in `col_to_letter`.
- **tests/test_excel_dashboard.py** – Added test for negative column index handling.
- **modules/data/fetching.py** – Added timeout parameter to FMP request.
- **modules/generate_report/fallback_data.py** – Added timeouts for all HTTP calls.
- **modules/generate_report/metadata_checker.py** – Added timeouts for FMP requests.
- **modules/management/group_analysis/group_analysis.py** – Added timeout to Directus POST request.
- **modules/management/portfolio_manager/portfolio_manager.py** – Added timeout to Directus POST request.
- **tests/test_fetching.py** – Added test ensuring FMP requests include timeout.
- **tests/test_fallback_data.py** – Updated mocks to accept timeout argument.
- **tests/test_metadata_checker.py** – Updated mocks to accept timeout argument.
- **modules/data/directus_mapper.py** – Added `TYPE_CHECKING` import and optional
  pandas import for type hints, fixing flake8 undefined-name warning.
- **scripts/main.py** – Removed unused `logging` import.
- **scripts/sync_directus_fields.py** – Dropped unused `json` import and retained
  `MAP_FILE` export for tests.
- **tests/test_sync_directus_fields.py** – Removed unused `Path` import.

## Remaining Warnings/TODOs
- No outstanding warnings.

## Additional Updates
- Fixed fetch_and_compile default output to respect OUTPUT_DIR when DIRECTUS_URL is set.
- Updated portfolio_manager to only sync with Directus when token is available.
- All tests passing.

### Latest Changes
- **modules/generate_report/report_generator.py** – Removed stray merge markers causing an `IndentationError`.
- **agent.md** – Updated with latest automated test results.
- All tests continue to pass with no errors.
