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
