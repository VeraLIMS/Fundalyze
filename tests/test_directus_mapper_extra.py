"""Additional mapping scenarios for Directus utilities."""
import json
import pandas as pd
import modules.data.directus_mapper as dm
import importlib


def test_ensure_field_mapping_new(monkeypatch, tmp_path):
    mapping = {"collections": {"stocks": {"fields": {"A": {"mapped_to": "a"}}}}}
    file = tmp_path / "directus_field_map.json"
    file.write_text(json.dumps(mapping))
    monkeypatch.setattr(dm, "MAP_FILE", file)
    monkeypatch.setattr(dm, "list_fields", lambda c: ["a", "b", "c"])
    inputs = iter(["c"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))
    df = pd.DataFrame(columns=["A", "C"])
    dm.ensure_field_mapping("stocks", df)
    data = json.loads(file.read_text())
    assert data["collections"]["stocks"]["fields"]["C"]["mapped_to"] == "c"


def test_ensure_field_mapping_invalid(monkeypatch, tmp_path):
    mapping = {"collections": {"stocks": {"fields": {"A": {"mapped_to": "x"}}}}}
    file = tmp_path / "directus_field_map.json"
    file.write_text(json.dumps(mapping))
    monkeypatch.setattr(dm, "MAP_FILE", file)
    monkeypatch.setattr(dm, "list_fields", lambda c: ["a", "b"])
    inputs = iter(["a"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))
    df = pd.DataFrame(columns=["A"])
    dm.ensure_field_mapping("stocks", df)
    data = json.loads(file.read_text())
    assert data["collections"]["stocks"]["fields"]["A"]["mapped_to"] == "a"


def test_cli_add_missing_mappings(monkeypatch, tmp_path):
    mapping = {"collections": {"stocks": {"fields": {"A": {"mapped_to": "a"}}}}}
    file = tmp_path / "directus_field_map.json"
    file.write_text(json.dumps(mapping))
    monkeypatch.setattr(dm, "MAP_FILE", file)

    module = importlib.import_module("scripts.add_missing_mappings")
    monkeypatch.setattr(module.dm, "MAP_FILE", file)

    rec = tmp_path / "rec.json"
    rec.write_text(json.dumps({"A": 1, "B": 2}))

    module.main(["stocks", str(rec)])

    data = json.loads(file.read_text())
    assert "B" in data["collections"]["stocks"]["fields"]

