"""Tests for FinanceAPIConfig and FinanceAPIClient."""

from pathlib import Path
from types import SimpleNamespace

import pytest

from modules.data.finance_api import FinanceAPIConfig, FinanceAPIClient


def test_config_load(tmp_path: Path) -> None:
    cfg_file = tmp_path / "finance_api.yaml"
    cfg_file.write_text(
        """
base_url: https://example.com/api
api_key: token123
endpoints:
  profile: /p/{symbol}
"""
    )

    cfg = FinanceAPIConfig.load(cfg_file)
    assert cfg.base_url == "https://example.com/api"
    assert cfg.api_key == "token123"
    assert cfg.endpoints["profile"] == "/p/{symbol}"


def test_client_builds_url_and_fetches(monkeypatch):
    cfg = FinanceAPIConfig(
        base_url="https://api.test", api_key="ABC", endpoints={"profile": "/pro/{symbol}"}
    )
    called = {}

    def fake_get(url, timeout):
        called["url"] = url
        called["timeout"] = timeout
        return SimpleNamespace(json=lambda: {"ok": True}, raise_for_status=lambda: None)

    monkeypatch.setattr("modules.data.finance_api.requests.get", fake_get)
    client = FinanceAPIClient(cfg, timeout=5)
    result = client.get_profile("XYZ")

    assert result == {"ok": True}
    assert called["url"] == "https://api.test/pro/XYZ?apikey=ABC"
    assert called["timeout"] == 5


def test_missing_endpoint():
    cfg = FinanceAPIConfig(base_url="x", endpoints={})
    client = FinanceAPIClient(cfg)
    with pytest.raises(KeyError):
        client.get_profile("ABC")

