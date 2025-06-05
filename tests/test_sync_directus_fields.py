import importlib
import json

import modules.data.directus_mapper as dm


def test_sync_add_collection_and_field(monkeypatch, tmp_path):
    file = tmp_path / "directus_field_map.json"
    file.write_text(json.dumps({"collections": {}}))
    monkeypatch.setattr(dm, "MAP_FILE", file)

    monkeypatch.setattr(dm, "MAP_FILE", file)
    monkeypatch.setenv("DIRECTUS_URL", "http://api")
    import modules.data.directus_client as dc
    monkeypatch.setattr(dc, "DIRECTUS_URL", "http://api")

    monkeypatch.setattr(
        dm, "list_collections", lambda: ["stocks"]
    )
    monkeypatch.setattr(
        dm, "list_fields_with_types", lambda c: [
            {"field": "id", "type": "integer"},
            {"field": "name", "type": "string"},
        ]
    )

    module = importlib.import_module("scripts.sync_directus_fields")
    monkeypatch.setattr(module, "list_collections", lambda: ["stocks"])
    monkeypatch.setattr(
        module,
        "list_fields_with_types",
        lambda c: [
            {"field": "id", "type": "integer"},
            {"field": "name", "type": "string"},
        ],
    )
    inputs = iter(["", "", "yes"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))
    monkeypatch.setattr(module, "MAP_FILE", file)
    monkeypatch.setattr(module, "load_field_map", dm.load_field_map)
    monkeypatch.setattr(module, "save_field_map", dm.save_field_map)
    module.main()

    data = json.loads(file.read_text())
    assert data["collections"]["stocks"]["fields"]["id"]["mapped_to"] == "id"
    assert "name" in data["collections"]["stocks"]["fields"]


def test_sync_handle_deletion_and_type_change(monkeypatch, tmp_path):
    mapping = {
        "collections": {
            "stocks": {
                "fields": {
                    "id": {"type": "integer", "mapped_to": "id"},
                    "name": {"type": "string", "mapped_to": "name"},
                }
            }
        }
    }
    file = tmp_path / "directus_field_map.json"
    file.write_text(json.dumps(mapping))
    monkeypatch.setattr(dm, "MAP_FILE", file)

    import modules.data.directus_client as dc
    monkeypatch.setattr(dc, "DIRECTUS_URL", "http://api")

    module = importlib.import_module("scripts.sync_directus_fields")
    monkeypatch.setattr(module, "list_collections", lambda: ["stocks"])
    monkeypatch.setattr(module, "list_fields_with_types", lambda c: [{"field": "id", "type": "string"}])

    inputs = iter(["yes", "yes", "yes"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))
    monkeypatch.setattr(module, "MAP_FILE", file)
    monkeypatch.setattr(module, "load_field_map", dm.load_field_map)
    monkeypatch.setattr(module, "save_field_map", dm.save_field_map)
    module.main()

    data = json.loads(file.read_text())
    fields = data["collections"]["stocks"]["fields"]
    assert "name" not in fields
    assert fields["id"]["type"] == "string"
