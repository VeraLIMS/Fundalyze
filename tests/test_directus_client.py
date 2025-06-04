from unittest.mock import MagicMock

import modules.data.directus_client as dc


def test_headers_with_token(monkeypatch):
    monkeypatch.setattr(dc, "DIRECTUS_TOKEN", "abc")
    assert dc._headers() == {"Authorization": "Bearer abc"}


def test_headers_no_token(monkeypatch):
    monkeypatch.setattr(dc, "DIRECTUS_TOKEN", None)
    assert dc._headers() == {}


def test_list_fields(monkeypatch):
    monkeypatch.setattr(dc, "DIRECTUS_URL", "http://api")
    resp = MagicMock()
    resp.json.return_value = {"data": [{"field": "a"}, {"field": "b"}]}
    resp.raise_for_status.return_value = None
    monkeypatch.setattr(dc.requests, "get", lambda url, headers: resp)
    fields = dc.list_fields("col")
    assert fields == ["a", "b"]


def test_fetch_items(monkeypatch):
    monkeypatch.setattr(dc, "DIRECTUS_URL", "http://api")
    resp = MagicMock()
    resp.json.return_value = {"data": [{"x": 1}]}
    resp.raise_for_status.return_value = None
    monkeypatch.setattr(dc.requests, "get", lambda url, headers: resp)
    items = dc.fetch_items("col")
    assert items == [{"x": 1}]


def test_insert_items(monkeypatch):
    monkeypatch.setattr(dc, "DIRECTUS_URL", "http://api")
    resp = MagicMock()
    resp.json.return_value = {"data": [1]}
    resp.raise_for_status.return_value = None
    monkeypatch.setattr(dc.requests, "post", lambda url, json, headers: resp)
    res = dc.insert_items("col", [1])
    assert res == [1]

def test_requires_url(monkeypatch):
    monkeypatch.setattr(dc, "DIRECTUS_URL", None)
    try:
        dc.list_fields("col")
    except RuntimeError:
        assert True
    else:
        assert False
