# UI Improvement Report

The Fundalyze project uses a command line interface exposed via `scripts/main.py` and various management modules. The following usability issues were identified:

- **Inconsistent error messages and prompts**: menus printed varying phrases like "Invalid choice", "Invalid selection" or numeric ranges (e.g. `Enter 1/2/3/4/5`).
- **Lack of clear cancel instructions** when adding tickers or groups.
- **Minimal CLI help**: the main entry script lacked usage examples and a version flag.

## Refactoring Steps

1. Added a helper in `modules/interface.py` for standardized invalid choice messages.
2. Updated all interactive modules to import `print_invalid_choice` and replaced bespoke messages.
3. Clarified prompts for adding tickers to mention pressing Enter to cancel.
4. Revised menu prompts to use `Select an option [n]` wording.
5. Enhanced `scripts/main.py` argument parser with examples, version flag and `RawTextHelpFormatter`.

## Affected Files

- `modules/interface.py`
- `scripts/main.py`
- `modules/management/portfolio_manager/portfolio_manager.py`
- `modules/management/group_analysis/group_analysis.py`
- `modules/management/note_manager/note_manager.py`
- `modules/management/directus_tools/directus_wizard.py`
- `modules/management/settings_manager/settings_manager.py`
- `modules/management/settings_manager/wizards/timezone.py`
- `modules/generate_report/__init__.py`

These changes ensure consistent feedback across the CLI and provide clearer guidance for new users.

### Additional Updates

- Refined `INVALID_CHOICE_MSG` in `modules/interface.py` to instruct users to
  press `Ctrl+C` for exit.
- Standardised all menu prompts to use the `Select an option [n]` pattern for
  clarity.
- Added subcommand descriptions in `scripts/main.py` so `--help` shows a brief
  explanation for each command.

### Latest Updates

- Added `print_header` helper in `modules/interface.py` for consistent section
  headings and expanded `INVALID_CHOICE_MSG` to mention running the help flag.
- Updated menu headers in `scripts/main.py`, `group_analysis.py`, `note_manager.py`
  and report generation to use `print_header`.
- Fixed prompt wording in `modules/generate_report/__init__.py` and standardized
  group-selection messages to the `[1-n]` format.
- Improved note creation flow to allow cancellation with Enter or 'q'.

### Recent Updates

- Fixed CLI crash when running `scripts/main.py` due to missing
  `run_metadata_checker` export. Added a backwards compatible alias in
  `modules/generate_report/__init__.py` at line 8.
- Clarified group creation prompts in
  `modules/management/group_analysis/group_analysis.py` lines
  205–219 to mention pressing Enter to cancel selections.

### New Enhancements

- Standardized menu headings by calling `print_header` in
  `portfolio_manager.py`, `settings_manager.py` and `directus_wizard.py`.
- Added cancel options for removing tickers and deleting groups:
  - `portfolio_manager.remove_ticker` lines 245–253 allow pressing Enter to cancel.
  - `group_analysis.remove_ticker_from_group` lines 296–316 handle empty input.
  - `group_analysis.delete_group` lines 340–347 handle empty input.
- Viewing notes now accepts an empty title to cancel in
  `note_manager.py` lines 78–81.
- Settings modifications can be canceled by leaving the key blank in
  `settings_manager.py` lines 58–66 and 80–88.

### Latest Enhancements

- Added a chart emoji to the group analysis header for consistent styling in
  `group_analysis.py` line 376.
- Allow canceling group selection when adding tickers; see
  `group_analysis.py` lines 415–423.
- The timezone wizard now accepts an empty response to cancel in
  `timezone.py` lines 23–28.

### New Fixes

- `scripts/run_tests.py` now provides `--help` and an optional glob pattern.
  See lines 11–28 and 32–36 for the argument parser.
- `scripts/note_cli.py` injects `sys.path` so running the script directly works
  and exposes a help flag. See lines 4–27.
