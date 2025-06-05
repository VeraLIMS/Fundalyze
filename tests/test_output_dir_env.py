"""Validate OUTPUT_DIR environment variable handling."""
import pandas as pd

import modules.generate_report.report_generator as rg
import modules.generate_report.excel_dashboard as ed
from tests.helpers import Dummy, make_fake_obb


def test_env_output_dir(tmp_path, monkeypatch):
    profile_df = pd.DataFrame({"symbol": ["AAA"]})
    price_df = pd.DataFrame({"Date": pd.date_range("2023-01-01", periods=1)})
    stmt_df = pd.DataFrame({"Revenue": [1]}, index=pd.Index(["2023"], name="Period"))

    monkeypatch.setattr(
        rg,
        "obb",
        make_fake_obb(profile_df=profile_df, price_df=price_df, stmt_df=stmt_df),
    )
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    rg.fetch_and_compile("AAA")
    assert (tmp_path / "AAA" / "profile.csv").is_file()

    dash = ed.create_dashboard()
    assert dash.is_file()


def test_fetch_and_compile_custom_period(tmp_path, monkeypatch):
    """Ensure custom price_period is forwarded to OpenBB"""

    profile_df = pd.DataFrame({"symbol": ["AAA"]})
    price_df = pd.DataFrame({"Date": pd.date_range("2023-01-01", periods=1)})
    calls = {}

    monkeypatch.setattr(
        rg,
        "obb",
        make_fake_obb(
            profile_df=profile_df, price_df=price_df, stmt_df=price_df, calls=calls
        ),
    )
    rg.fetch_and_compile("AAA", base_output=str(tmp_path), price_period="5d")
    assert calls.get("period") == "5d"
