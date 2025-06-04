import pandas as pd
import modules.management.group_analysis.group_analysis as ga


def test_load_groups_directus(monkeypatch):
    records = [{"Group": "G", "Ticker": "AAA", "Name": "Alpha"}]
    monkeypatch.setattr(ga, "USE_DIRECTUS", True)
    monkeypatch.setattr(ga, "fetch_items", lambda c: records)
    df = ga.load_groups("dummy.xlsx")
    assert list(df.columns) == ga.COLUMNS
    assert df.iloc[0]["Ticker"] == "AAA"


def test_save_groups_directus(monkeypatch):
    monkeypatch.setattr(ga, "USE_DIRECTUS", True)
    monkeypatch.setattr(ga, "list_fields", lambda c: ["Group", "Ticker", "Name"])
    captured = {}
    monkeypatch.setattr(ga, "insert_items", lambda c, recs: captured.setdefault("rec", recs))
    df = pd.DataFrame({"Group": ["G"], "Ticker": ["AAA"], "Name": ["Alpha"], "Extra": [1]})
    ga.save_groups(df, "dummy.xlsx")
    assert captured["rec"] == [{"Group": "G", "Ticker": "AAA", "Name": "Alpha"}]

