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

## Remaining Warnings/TODOs
- No outstanding warnings.
