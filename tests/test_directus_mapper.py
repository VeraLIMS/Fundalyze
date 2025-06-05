from pathlib import Path
import json
import modules.data.directus_mapper as dm


def test_map_file_location():
    repo_root = Path(__file__).resolve().parents[1]
    assert dm.MAP_FILE == repo_root / "config" / "directus_field_map.json"


def test_prepare_records(monkeypatch, tmp_path):
    mapping = {"companies": {"Ticker": "ticker_symbol", "Name": "company_name"}}
    file = tmp_path / "directus_field_map.json"
    file.write_text(json.dumps(mapping))
    monkeypatch.setattr(dm, "MAP_FILE", file)
    monkeypatch.setattr(dm, "list_fields", lambda c: ["ticker_symbol", "company_name"])

    records = [{"Ticker": "AAA", "Name": "Acme", "Extra": 1}]
    prepared = dm.prepare_records("companies", records)
    assert prepared == [{"ticker_symbol": "AAA", "company_name": "Acme"}]


def test_refresh_field_map(monkeypatch, tmp_path):
    file = tmp_path / "directus_field_map.json"
    monkeypatch.setattr(dm, "MAP_FILE", file)
    monkeypatch.setattr(dm, "list_collections", lambda: ["foo"])
    monkeypatch.setattr(dm, "list_fields", lambda c: ["a", "b"])

    mapping = dm.refresh_field_map()
    assert mapping == {"foo": {"a": "a", "b": "b"}}
    # Add new field on second call
    monkeypatch.setattr(dm, "list_fields", lambda c: ["a", "b", "c"])
    mapping2 = dm.refresh_field_map()
    assert mapping2 == {"foo": {"a": "a", "b": "b", "c": "c"}}
