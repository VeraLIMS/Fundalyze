import json
import modules.config_utils as config_utils


def test_load_settings_missing(tmp_path, monkeypatch):
    fake_path = tmp_path / "settings.json"
    monkeypatch.setattr(config_utils, "SETTINGS_PATH", fake_path)
    result = config_utils.load_settings()
    assert result == {}


def test_load_settings_with_file(tmp_path, monkeypatch):
    data = {"foo": 123, "bar": True}
    fake_path = tmp_path / "settings.json"
    fake_path.write_text(json.dumps(data))
    monkeypatch.setattr(config_utils, "SETTINGS_PATH", fake_path)
    result = config_utils.load_settings()
    assert result == data
