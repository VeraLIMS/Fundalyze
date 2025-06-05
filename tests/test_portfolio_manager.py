"""Tests for portfolio manager CLI operations."""
import pandas as pd
import modules.management.portfolio_manager.portfolio_manager as pm


def test_load_portfolio_local(monkeypatch):
    monkeypatch.setattr(pm, "USE_DIRECTUS", False)
    monkeypatch.setattr(pm.os.path, "isfile", lambda f: True)
    df = pd.DataFrame({"Ticker": ["A"], "Name": ["Acme"]})
    monkeypatch.setattr(pm.pd, "read_excel", lambda f, engine=None: df)
    result = pm.load_portfolio("dummy")
    assert "Ticker" in result.columns
    assert result.iloc[0]["Name"] == "Acme"


def test_load_portfolio_directus(monkeypatch):
    monkeypatch.setattr(pm, "USE_DIRECTUS", True)
    monkeypatch.setattr(pm, "fetch_items", lambda c: [{"Ticker": "A", "Name": "Acme"}])
    result = pm.load_portfolio("dummy")
    assert list(result.columns)[0] == "Ticker"
    assert result.iloc[0]["Name"] == "Acme"


def test_save_portfolio_directus(monkeypatch):
    monkeypatch.setattr(pm, "USE_DIRECTUS", True)
    monkeypatch.setattr(pm, "prepare_records", lambda c, recs: [recs[0]])
    records_holder = {}
    monkeypatch.setattr(pm, "insert_items", lambda c, recs: records_holder.setdefault('rec', recs))
    df = pd.DataFrame({"Ticker": ["A"], "Name": ["Acme"], "Extra": [1]})
    pm.save_portfolio(df, "dummy")
    assert records_holder['rec'] == [df.to_dict(orient="records")[0]]


def _mock_fetch(tk):
    return {
        "Ticker": tk,
        "Name": "Mock",
        "Sector": "Tech",
        "Industry": "Software",
        "Current Price": 1.0,
        "Market Cap": 1.0,
        "PE Ratio": 1.0,
        "Dividend Yield": 0.0,
    }


def test_existing_ticker_with_na_skips_adding(monkeypatch):
    df = pd.DataFrame([{c: pd.NA for c in pm.COLUMNS} for _ in range(2)])
    df.at[0, "Ticker"] = "HON"
    monkeypatch.setattr(pm, "fetch_from_yfinance", _mock_fetch)
    inputs = iter(["HON"])
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))
    result = pm.add_tickers(df)
    assert result["Ticker"].dropna().tolist() == ["HON"]


def test_add_new_ticker_with_nas_present(monkeypatch):
    df = pd.DataFrame([{c: pd.NA for c in pm.COLUMNS} for _ in range(2)])
    df.at[1, "Ticker"] = "AAPL"
    monkeypatch.setattr(pm, "fetch_from_yfinance", _mock_fetch)
    inputs = iter(["GOOG", "y"])
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))
    result = pm.add_tickers(df)
    assert set(result["Ticker"].dropna()) == {"AAPL", "GOOG"}


def test_add_ticker_to_all_na_column(monkeypatch):
    df = pd.DataFrame([{c: pd.NA for c in pm.COLUMNS} for _ in range(2)])
    monkeypatch.setattr(pm, "fetch_from_yfinance", _mock_fetch)
    inputs = iter(["MSFT", "y"])
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))
    result = pm.add_tickers(df)
    assert "MSFT" in result["Ticker"].dropna().tolist()


def test_load_portfolio_directus_all_na(monkeypatch):
    monkeypatch.setattr(pm, "USE_DIRECTUS", True)
    # Directus returns a blank record with all fields null
    monkeypatch.setattr(
        pm, "fetch_items", lambda c: [{"id": 1, "ticker": None, "name": None}]
    )
    df = pm.load_portfolio("dummy")
    assert df.empty
    assert list(df.columns) == pm.COLUMNS
