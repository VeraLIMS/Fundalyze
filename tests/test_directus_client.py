"""Tests for the Directus API client wrapper."""

import modules.data.directus_client as dc


def test_headers_with_token(monkeypatch):
    monkeypatch.setattr(dc, "DIRECTUS_TOKEN", "abc")
    monkeypatch.setattr(dc, "CF_ACCESS_CLIENT_ID", None)
    monkeypatch.setattr(dc, "CF_ACCESS_CLIENT_SECRET", None)
    assert dc._headers() == {"Authorization": "Bearer abc"}


def test_headers_no_token(monkeypatch):
    monkeypatch.setattr(dc, "DIRECTUS_TOKEN", None)
    monkeypatch.setattr(dc, "CF_ACCESS_CLIENT_ID", None)
    monkeypatch.setattr(dc, "CF_ACCESS_CLIENT_SECRET", None)
    assert dc._headers() == {}


def test_headers_cf_only(monkeypatch):
    monkeypatch.setattr(dc, "DIRECTUS_TOKEN", None)
    monkeypatch.setattr(dc, "CF_ACCESS_CLIENT_ID", "id")
    monkeypatch.setattr(dc, "CF_ACCESS_CLIENT_SECRET", "secret")
    assert dc._headers() == {
        "CF-Access-Client-Id": "id",
        "CF-Access-Client-Secret": "secret",
    }


def test_headers_token_and_cf(monkeypatch):
    monkeypatch.setattr(dc, "DIRECTUS_TOKEN", "abc")
    monkeypatch.setattr(dc, "CF_ACCESS_CLIENT_ID", "id")
    monkeypatch.setattr(dc, "CF_ACCESS_CLIENT_SECRET", "secret")
    assert dc._headers() == {
        "Authorization": "Bearer abc",
        "CF-Access-Client-Id": "id",
        "CF-Access-Client-Secret": "secret",
    }


def test_list_fields(monkeypatch):
    monkeypatch.setattr(dc, "DIRECTUS_URL", "http://api")
    monkeypatch.setattr(
        dc, "directus_request", lambda method, path, **kw: {"data": [{"field": "a"}, {"field": "b"}]}
    )
    fields = dc.list_fields("col")
    assert fields == ["a", "b"]


def test_list_fields_with_types(monkeypatch):
    monkeypatch.setattr(dc, "DIRECTUS_URL", "http://api")
    monkeypatch.setattr(
        dc,
        "directus_request",
        lambda m, p, **kw: {"data": [{"field": "a", "type": "string"}]},
    )
    fields = dc.list_fields_with_types("col")
    assert fields == [{"field": "a", "type": "string"}]


def test_fetch_items(monkeypatch):
    monkeypatch.setattr(dc, "DIRECTUS_URL", "http://api")
    monkeypatch.setattr(dc, "directus_request", lambda m, p, **kw: {"data": [{"x": 1}]})
    items = dc.fetch_items("col")
    assert items == [{"x": 1}]


def test_fetch_items_filtered(monkeypatch):
    monkeypatch.setattr(dc, "DIRECTUS_URL", "http://api")
    captured = {}

    def fake_request(method, path, **kw):
        captured["params"] = kw.get("params")
        return {"data": [{"x": 2}]}

    monkeypatch.setattr(dc, "directus_request", fake_request)
    items = dc.fetch_items_filtered("col", {"company_id": {"_eq": 1}})
    assert captured["params"] == {"filter": {"company_id": {"_eq": 1}}}
    assert items == [{"x": 2}]


def test_insert_items(monkeypatch):
    monkeypatch.setattr(dc, "DIRECTUS_URL", "http://api")
    called = {}

    def fake_request(method, path, **kw):
        called["method"] = method
        called["path"] = path
        called["payload"] = kw.get("json")
        return {"data": [1]}

    monkeypatch.setattr(dc, "directus_request", fake_request)
    res = dc.insert_items("col", [1])
    assert called["method"] == "POST"
    assert called["path"] == "items/col"
    assert called["payload"] == {"data": [1]}
    assert res == [1]


def test_list_collections(monkeypatch):
    monkeypatch.setattr(dc, "DIRECTUS_URL", "http://api")
    monkeypatch.setattr(
        dc, "directus_request", lambda m, p, **kw: {"data": [{"collection": "c1"}, {"collection": "c2"}]}
    )
    assert dc.list_collections() == ["c1", "c2"]


def test_create_field(monkeypatch):
    monkeypatch.setattr(dc, "DIRECTUS_URL", "http://api")
    captured = {}

    def fake_request(method, path, **kw):
        captured["method"] = method
        captured["path"] = path
        captured["json"] = kw.get("json")
        return {"data": {"field": "x"}}

    monkeypatch.setattr(dc, "directus_request", fake_request)
    result = dc.create_field("col", "x", "string")
    assert captured["method"] == "POST"
    assert captured["path"] == "fields/col"
    assert captured["json"]["field"] == "x"
    assert result == {"field": "x"}

def test_requires_url(monkeypatch):
    monkeypatch.setattr(dc, "DIRECTUS_URL", None)
    try:
        dc.list_fields("col")
    except RuntimeError:
        assert True
    else:
        assert False

def test_create_collection_if_missing_skips(monkeypatch):
    monkeypatch.setattr(dc, "DIRECTUS_URL", "http://api")
    monkeypatch.setattr(dc, "list_collections", lambda: ["col"])
    called = {}
    monkeypatch.setattr(dc, "directus_request", lambda *a, **k: called.setdefault("called", True))
    assert dc.create_collection_if_missing("col") is False
    assert "called" not in called


def test_create_collection_if_missing_creates(monkeypatch):
    monkeypatch.setattr(dc, "DIRECTUS_URL", "http://api")
    monkeypatch.setattr(dc, "list_collections", lambda: [])
    req = {}
    monkeypatch.setattr(dc, "directus_request", lambda m, p, **kw: req.update({"method": m, "path": p}) or {"data": {}})
    fields = []
    monkeypatch.setattr(dc, "create_field", lambda c, f: fields.append(f))
    created = dc.create_collection_if_missing("col", ["a", "b"])
    assert created is True
    assert req["path"] == "collections"
    assert set(fields) == {"a", "b"}


def test_insert_items_auto_creates(monkeypatch):
    monkeypatch.setattr(dc, "DIRECTUS_URL", "http://api")
    called = {}
    monkeypatch.setattr(dc, "create_collection_if_missing", lambda c, f=None: called.setdefault("called", True))
    monkeypatch.setattr(dc, "directus_request", lambda *a, **k: {"data": [1]})
    res = dc.insert_items("col", [{"x": 1}])
    assert "called" in called
    assert res == [1]
