import os
import sys
import pandas as pd
import importlib.util

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import modules.management.portfolio_manager.portfolio_manager as pm
pm.PORTFOLIO_FILE = "dummy"

spec = importlib.util.spec_from_file_location(
    "main", os.path.join(os.path.dirname(__file__), "..", "scripts", "main.py")
)
main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main)


def test_portfolio_summary_cli_empty(monkeypatch, capsys):
    monkeypatch.setattr(pm, "load_portfolio", lambda: pd.DataFrame())
    main.portfolio_summary_cli()
    out = capsys.readouterr().out
    assert "Portfolio is empty" in out


def test_portfolio_summary_cli_missing(monkeypatch, capsys):
    df = pd.DataFrame({
        "Ticker": ["A", "B"],
        "Current Price": [1.0, 2.0],
        "Sector": ["Tech", None],
    })
    monkeypatch.setattr(pm, "load_portfolio", lambda: df)
    main.portfolio_summary_cli()
    out = capsys.readouterr().out
    assert "Missing Fields:" in out
