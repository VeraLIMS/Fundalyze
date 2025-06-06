from requests import Response
import modules.data.directus_client as dc


def make_response(text, content_type="application/json"):
    resp = Response()
    resp.status_code = 200
    resp._content = text.encode("utf-8")
    resp.headers["content-type"] = content_type
    return resp


def test_parse_response_html():
    resp = make_response("<html></html>", "text/html")
    assert dc._parse_response(resp, "http://api") is None


def test_parse_response_invalid_json():
    resp = make_response("not json")
    assert dc._parse_response(resp, "http://api") is None


def test_parse_response_valid_json():
    resp = make_response('{"a": 1}')
    assert dc._parse_response(resp, "http://api") == {"a": 1}


def test_clean_record_nan_inf():
    record = {"a": 1.0, "b": float("nan"), "c": float("inf"), "d": float("-inf")}
    cleaned = dc.clean_record(record)
    assert cleaned["a"] == 1.0
    assert cleaned["b"] is None
    assert cleaned["c"] is None
    assert cleaned["d"] is None
