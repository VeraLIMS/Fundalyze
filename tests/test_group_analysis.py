"""Unit tests for group analysis CLI tool."""
import pandas as pd
import modules.management.group_analysis.group_analysis as ga


def test_load_groups_directus(monkeypatch):
    records = [{"Group": "G", "Ticker": "AAA", "Name": "Alpha"}]
    monkeypatch.setattr(ga, "fetch_items", lambda c: records)
    df = ga.load_groups()
    assert list(df.columns) == ga.COLUMNS
    assert df.iloc[0]["Ticker"] == "AAA"


def test_save_groups_directus(monkeypatch):
    monkeypatch.setattr(ga, "prepare_records", lambda c, recs: [recs[0]])
    captured = {}
    monkeypatch.setattr(ga, "insert_items", lambda c, recs: captured.setdefault("rec", recs))
    df = pd.DataFrame({"Group": ["G"], "Ticker": ["AAA"], "Name": ["Alpha"], "Extra": [1]})
    ga.save_groups(df)
    assert captured["rec"] == [df.to_dict(orient="records")[0]]


def test_confirm_or_adjust_ticker_yes(monkeypatch):
    inputs = iter(["y"])
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))
    assert ga.confirm_or_adjust_ticker("AAA") == "AAA"


def test_confirm_or_adjust_ticker_no_change(monkeypatch):
    inputs = iter(["n", "BBB"])
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))
    assert ga.confirm_or_adjust_ticker("AAA") == "BBB"


def test_confirm_or_adjust_ticker_cancel(monkeypatch):
    inputs = iter(["maybe", "n", ""])
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))
    assert ga.confirm_or_adjust_ticker("AAA") == ""


def test_choose_group_with_portfolio(monkeypatch):
    df = pd.DataFrame({"Ticker": ["AAA", "BBB"]})
    inputs = iter(["1"])
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))
    assert ga.choose_group(df) == "AAA"


def test_choose_group_custom(monkeypatch):
    df = pd.DataFrame({"Ticker": ["AAA"]})
    inputs = iter(["2", "MyGrp"])
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))
    assert ga.choose_group(df) == "MyGrp"


def test_choose_group_empty(monkeypatch):
    df = pd.DataFrame()
    inputs = iter(["GroupX"])
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))
    assert ga.choose_group(df) == "GroupX"


def test_load_groups_directus_all_na(monkeypatch):
    monkeypatch.setattr(ga, "fetch_items", lambda c: [{"id": 1, "group": None, "ticker": None}])
    df = ga.load_groups()
    assert df.empty
    assert list(df.columns) == ga.COLUMNS

