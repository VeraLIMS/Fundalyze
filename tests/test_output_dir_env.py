"""Validate OUTPUT_DIR environment variable handling."""
import pandas as pd

import modules.generate_report.report_generator as rg
import modules.generate_report.excel_dashboard as ed

class Dummy:
    def __init__(self, df):
        self._df = df

    def to_df(self):
        return self._df


def test_env_output_dir(tmp_path, monkeypatch):
    profile_df = pd.DataFrame({"symbol": ["AAA"]})
    price_df = pd.DataFrame({"Date": pd.date_range("2023-01-01", periods=1)})
    stmt_df = pd.DataFrame({"Revenue": [1]}, index=pd.Index(["2023"], name="Period"))

    class FakeEquity:
        def __init__(self):
            class _Profile:
                def __call__(self, symbol):
                    return Dummy(profile_df)

            class _Price:
                def historical(self, symbol, period, provider=None):
                    return Dummy(price_df)

            class _Fundamental:
                def income(self, symbol, period):
                    return Dummy(stmt_df)

                def balance(self, symbol, period):
                    return Dummy(stmt_df)

                def cash(self, symbol, period):
                    return Dummy(stmt_df)

            self.profile = _Profile()
            self.price = _Price()
            self.fundamental = _Fundamental()

    class FakeOBB:
        def __init__(self):
            self.equity = FakeEquity()

    monkeypatch.setattr(rg, "obb", FakeOBB())
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

    class FakeEquity:
        def __init__(self):
            class _Profile:
                def __call__(self, symbol):
                    return Dummy(profile_df)

            class _Price:
                def historical(self, symbol, period, provider=None):
                    calls["period"] = period
                    return Dummy(price_df)

            class _Fundamental:
                def income(self, symbol, period):
                    return Dummy(price_df)

                def balance(self, symbol, period):
                    return Dummy(price_df)

                def cash(self, symbol, period):
                    return Dummy(price_df)

            self.profile = _Profile()
            self.price = _Price()
            self.fundamental = _Fundamental()

    class FakeOBB:
        def __init__(self):
            self.equity = FakeEquity()

    monkeypatch.setattr(rg, "obb", FakeOBB())
    rg.fetch_and_compile("AAA", base_output=str(tmp_path), price_period="5d")
    assert calls.get("period") == "5d"
