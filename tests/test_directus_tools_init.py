"""Ensure directus_tools exposes run_directus_wizard."""
import inspect

from modules.management.directus_tools import run_directus_wizard
from modules.management.directus_tools import directus_wizard as dw


def test_run_directus_wizard_export():
    assert run_directus_wizard is dw.run_directus_wizard
    assert inspect.isfunction(run_directus_wizard)
