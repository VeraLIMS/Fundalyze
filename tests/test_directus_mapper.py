"""Tests for Directus schema mapping."""
from pathlib import Path
import json
import pytest
import modules.data.directus_mapper as dm


def test_map_file_location():
    repo_root = Path(__file__).resolve().parents[1]
    assert dm.MAP_FILE == repo_root / "config" / "directus_field_map.json"


def test_prepare_records(monkeypatch, tmp_path):
    mapping = {
        "collections": {
            "companies": {
                "fields": {
                    "Ticker": {"type": "string", "mapped_to": "ticker"},
                    "Name": {"type": "string", "mapped_to": "name"},
                }
            }
        }
    }
    file = tmp_path / "directus_field_map.json"
    file.write_text(json.dumps(mapping))
    monkeypatch.setattr(dm, "MAP_FILE", file)
    monkeypatch.setattr(dm, "list_fields", lambda c: ["ticker", "name"])

    records = [{"Ticker": "AAA", "Name": "Acme", "Extra": 1}]
    prepared = dm.prepare_records("companies", records)
    assert prepared == [{"ticker": "AAA", "name": "Acme"}]


def test_interactive_prepare_records(monkeypatch, tmp_path):
    mapping = {"collections": {"reports": {"fields": {"Ticker": {"mapped_to": "symbol", "type": "string"}}}}}
    file = tmp_path / "directus_field_map.json"
    file.write_text(json.dumps(mapping))
    monkeypatch.setattr(dm, "MAP_FILE", file)
    monkeypatch.setattr(dm, "list_fields", lambda c: ["symbol", "value"])

    inputs = iter(["value"])
    monkeypatch.setattr("builtins.input", lambda *a: next(inputs))

    records = [{"Ticker": "HON", "Metric": 1}]
    prepared = dm.interactive_prepare_records("reports", records)
    assert prepared == [{"symbol": "HON", "value": 1}]
    saved = json.loads(file.read_text())
    assert saved["collections"]["reports"]["fields"]["Metric"]["mapped_to"] == "value"


def test_refresh_field_map(monkeypatch, tmp_path):
    file = tmp_path / "directus_field_map.json"
    monkeypatch.setattr(dm, "MAP_FILE", file)
    monkeypatch.setattr(dm, "list_collections", lambda: ["foo"])
    monkeypatch.setattr(
        dm, "list_fields_with_types", lambda c: [
            {"field": "a", "type": "string"},
            {"field": "b", "type": "integer"},
        ]
    )

    mapping = dm.refresh_field_map()
    assert mapping == {
        "collections": {
            "foo": {
                "fields": {
                    "a": {"type": "string", "mapped_to": "a"},
                    "b": {"type": "integer", "mapped_to": "b"},
                }
            }
        }
    }
    # Add new field on second call
    monkeypatch.setattr(
        dm,
        "list_fields_with_types",
        lambda c: [
            {"field": "a", "type": "string"},
            {"field": "b", "type": "integer"},
            {"field": "c", "type": "text"},
        ],
    )
    mapping2 = dm.refresh_field_map()
    assert "c" in mapping2["collections"]["foo"]["fields"]


def test_prepare_records_empty(monkeypatch, tmp_path):
    mapping = {"collections": {"portfolio": {"fields": {}}}}
    file = tmp_path / "directus_field_map.json"
    file.write_text(json.dumps(mapping))
    monkeypatch.setattr(dm, "MAP_FILE", file)
    monkeypatch.setattr(dm, "list_fields", lambda c: ["ticker"])

    with pytest.raises(ValueError):
        dm.prepare_records("portfolio", [{"Ticker": "AAPL"}])
