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
