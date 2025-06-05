"""Verify management package exports CLI entry points."""
from modules.management import (
    run_portfolio_manager,
    run_group_analysis,
    run_note_manager,
    run_settings_manager,
    run_directus_wizard,
)


def test_management_exports_callable():
    assert callable(run_portfolio_manager)
    assert callable(run_group_analysis)
    assert callable(run_note_manager)
    assert callable(run_settings_manager)
    assert callable(run_directus_wizard)
