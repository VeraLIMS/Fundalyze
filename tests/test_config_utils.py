"""Unit tests for configuration loading utilities."""
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


def test_save_settings(tmp_path, monkeypatch):
    fake_path = tmp_path / "settings.json"
    monkeypatch.setattr(config_utils, "SETTINGS_PATH", fake_path)
    data = {"foo": "bar"}
    config_utils.save_settings(data)
    assert json.loads(fake_path.read_text()) == data


def test_env_roundtrip(tmp_path, monkeypatch):
    fake_env = tmp_path / ".env"
    monkeypatch.setattr(config_utils, "ENV_PATH", fake_env)
    env = {"A": "1", "B": "two"}
    config_utils.save_env(env)
    loaded = config_utils.load_env()
    assert loaded == env
