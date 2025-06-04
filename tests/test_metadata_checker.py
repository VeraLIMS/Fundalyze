import pandas as pd
from unittest.mock import MagicMock
import pytest

import modules.generate_report.metadata_checker as mc


def test_iso_timestamp_utc_format():
    ts = mc.iso_timestamp_utc()
    assert "T" in ts and ts.endswith("Z")


def test_fetch_profile_from_yf_basic(monkeypatch):
    info = {
        "longName": "Acme Corp",
        "sector": "Tech",
        "industry": "Software",
        "marketCap": 100,
        "website": "example.com",
        "currentPrice": 10,
    }

    class FakeTicker:
        def __init__(self, info):
            self.info = info

    monkeypatch.setattr(mc.yf, "Ticker", lambda s: FakeTicker(info))
    df = mc.fetch_profile_from_yf("AAA")
    assert df.iloc[0]["sector"] == "Tech"
    assert df.iloc[0]["symbol"] == "AAA"


def test_fetch_profile_from_yf_fmp_fallback(monkeypatch):
    class FakeTicker:
        info = {}

    monkeypatch.setattr(mc.yf, "Ticker", lambda s: FakeTicker())
    resp = MagicMock()
    resp.json.return_value = [{
        "symbol": "AAA",
        "companyName": "Acme Corp",
        "sector": "Tech",
        "industry": "Software",
        "mktCap": 100,
        "website": "example.com",
    }]
    resp.raise_for_status.return_value = None
    monkeypatch.setattr(mc.requests, "get", lambda url: resp)

    df = mc.fetch_profile_from_yf("AAA")
    assert df.iloc[0]["sector"] == "Tech"
    assert df.iloc[0]["website"] == "example.com"


def test_fetch_fmp_statement(monkeypatch):
    resp = MagicMock()
    resp.json.return_value = [{"date": "2023", "Revenue": 5}]
    resp.raise_for_status.return_value = None
    monkeypatch.setattr(mc.requests, "get", lambda url: resp)
    df = mc.fetch_fmp_statement("AAA", "income-statement", "annual")
    assert df.index.name == "date"
    assert df.loc["2023", "Revenue"] == 5
