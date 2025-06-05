
import modules.data.directus_client as dc


def test_headers_with_token(monkeypatch):
    monkeypatch.setattr(dc, "DIRECTUS_TOKEN", "abc")
    assert dc._headers() == {"Authorization": "Bearer abc"}


def test_headers_no_token(monkeypatch):
    monkeypatch.setattr(dc, "DIRECTUS_TOKEN", None)
    assert dc._headers() == {}


def test_list_fields(monkeypatch):
    monkeypatch.setattr(dc, "DIRECTUS_URL", "http://api")
    monkeypatch.setattr(
        dc, "directus_request", lambda method, path, **kw: {"data": [{"field": "a"}, {"field": "b"}]}
    )
    fields = dc.list_fields("col")
    assert fields == ["a", "b"]


def test_fetch_items(monkeypatch):
    monkeypatch.setattr(dc, "DIRECTUS_URL", "http://api")
    monkeypatch.setattr(dc, "directus_request", lambda m, p, **kw: {"data": [{"x": 1}]})
    items = dc.fetch_items("col")
    assert items == [{"x": 1}]


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
