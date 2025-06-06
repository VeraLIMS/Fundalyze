# Management Tools

This document explains the command line utilities under `modules/management` and how to interact with them. Each tool exposes a simple menu-driven interface and can be launched either via `scripts/main.py` or by importing the appropriate function.

```
modules/management
├── portfolio_manager/
│   └── portfolio_manager.py
├── group_analysis/
│   └── group_analysis.py
├── note_manager/
│   └── note_manager.py
├── settings_manager/
│   ├── settings_manager.py
│   └── wizards/
│       ├── directus_setup.py
│       ├── notes_dir.py
│       ├── openbb_key.py
│       ├── fmp_key.py
│       ├── openai_key.py
│       ├── output_dir.py
│       ├── timezone.py
│       ├── cf_access.py
│       └── quick_setup.py
└── directus_tools/
    └── directus_wizard.py
```

## Portfolio Manager
Launch with `run_portfolio_manager()` or directly:
```bash
python modules/management/portfolio_manager/portfolio_manager.py
```
The menu allows you to view your portfolio, add or update tickers, and remove entries. Data is stored directly in your configured Directus collection. When adding tickers the script attempts to fetch data from yfinance and prompts for confirmation or manual entry if anything is missing.

## Group Analysis
Run via `run_group_analysis()`. Groups are saved in a Directus collection and can be linked to portfolio tickers or given a custom name. You can create groups, add or remove tickers, and delete entire groups. The workflow mirrors the portfolio manager but operates on a "Group" column in the database.

## Note Manager
`run_note_manager()` provides a minimal Markdown note system. Each note is stored as a `.md` file under the directory specified by `NOTES_DIR` (defaults to `notes/`). The CLI lets you list notes, view contents (showing any `[[wikilink]]` references) and create new notes interactively. Enter an empty title or choose "Return" to cancel an action.

## Settings Manager
Use `run_settings_manager()` to edit `config/settings.json` or `.env`. The tool exposes submenus for general settings, environment variables and setup wizards. Helper functions validate input, allow cancellation on blank entries and ensure the configuration directory exists.

## Directus Tools
`run_directus_wizard()` exposes common Directus API operations like listing collections, viewing or creating fields and inserting items. The wizard checks that `DIRECTUS_URL` and a token are configured, otherwise it offers to run the Directus setup wizard.

These management utilities are intentionally lightweight so they can be extended easily. See `docs/DEVELOPER_GUIDE.md` for guidelines on adding new commands.
