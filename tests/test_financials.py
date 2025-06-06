import pandas as pd
import modules.data.financials as fin

class Dummy:
    def __init__(self, df):
        self._df = df
    def to_df(self):
        return self._df

class DummyFundamental:
    def __init__(self, df):
        self.income = lambda symbol, period: Dummy(df)
        self.balance = lambda symbol, period: Dummy(df)
        self.cash = lambda symbol, period: Dummy(df)

class DummyEquity:
    def __init__(self, df):
        self.fundamental = DummyFundamental(df)

class DummyOBB:
    def __init__(self, df):
        self.equity = DummyEquity(df)


def test_fetch_statements(monkeypatch):
    df = pd.DataFrame({"A": ["1B"]}, index=["2024"])
    obb = DummyOBB(df)
    monkeypatch.setattr(fin, "get_openbb", lambda: obb)
    result = fin.fetch_statements("AAA")
    assert result["income"]["annual"].iloc[0, 0] == 1_000_000_000


def test_store_statements(monkeypatch):
    captured = {}
    monkeypatch.setattr(fin, "prepare_records", lambda c, r: r)
    monkeypatch.setattr(fin, "insert_items", lambda col, rec: captured.setdefault(col, []).extend(rec))
    data = {"income": {"annual": pd.DataFrame({"A": [1]}, index=["2024"]), "quarter": pd.DataFrame()},
            "balance": {"annual": pd.DataFrame(), "quarter": pd.DataFrame()}}
    fin.store_statements(data)
    assert "income_statement" in captured
    assert captured["income_statement"][0]["period"] == "2024"


def test_fetch_and_store_statements(monkeypatch):
    df = pd.DataFrame({"A": [1]}, index=["2024"])
    obb = DummyOBB(df)
    monkeypatch.setattr(fin, "get_openbb", lambda: obb)
    monkeypatch.setattr(fin, "prepare_records", lambda c, r: r)
    inserted = {}
    monkeypatch.setattr(fin, "insert_items", lambda c, r: inserted.setdefault(c, []).extend(r))
    fin.fetch_and_store_statements("ZZZ", statements=["income"])
    assert inserted["income_statement"][0]["A"] == 1

