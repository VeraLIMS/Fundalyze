"""Tests for metadata_checker re-fetch workflow."""
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
    monkeypatch.setattr(mc.requests, "get", lambda url, **kwargs: resp)

    df = mc.fetch_profile_from_yf("AAA")
    assert df.iloc[0]["sector"] == "Tech"
    assert df.iloc[0]["website"] == "example.com"


def test_fetch_fmp_statement(monkeypatch):
    resp = MagicMock()
    resp.json.return_value = [{"date": "2023", "Revenue": 5}]
    resp.raise_for_status.return_value = None
    monkeypatch.setattr(mc.requests, "get", lambda url, **kwargs: resp)
    df = mc.fetch_fmp_statement("AAA", "income-statement", "annual")
    assert df.index.name == "date"
    assert df.loc["2023", "Revenue"] == 5


def test_fetch_1mo_prices_yf_history(monkeypatch):
    dates = pd.date_range("2023-01-01", periods=2, freq="D")
    hist = pd.DataFrame(
        {
            "Open": [1, 2],
            "High": [1, 2],
            "Low": [1, 2],
            "Close": [1, 2],
            "Adj Close": [1, 2],
            "Volume": [10, 20],
            "Dividends": [0, 0],
            "Stock Splits": [0, 0],
        },
        index=dates,
    )
    hist.index.name = "Date"

    class FakeTicker:
        def history(self, period="1mo"):
            return hist

    monkeypatch.setattr(mc.yf, "Ticker", lambda s: FakeTicker())
    monkeypatch.setattr(mc.yf, "download", lambda *a, **k: pytest.fail("download called"))

    result = mc.fetch_1mo_prices_yf("AAA")
    assert list(result.columns) == ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
    assert len(result) == 2
    assert result.iloc[0]["Date"] == dates[0]


def test_fetch_1mo_prices_yf_download_fallback(monkeypatch):
    class FakeTicker:
        def history(self, period="1mo"):
            return pd.DataFrame()

    dates = pd.date_range("2023-02-01", periods=1, freq="D")
    dl_df = pd.DataFrame(
        {
            "Open": [5],
            "High": [6],
            "Low": [4],
            "Close": [5],
            "Adj Close": [5],
            "Volume": [30],
        },
        index=dates,
    )
    dl_df.index.name = "Date"

    monkeypatch.setattr(mc.yf, "Ticker", lambda s: FakeTicker())
    monkeypatch.setattr(mc.yf, "download", lambda symbol, period: dl_df)

    result = mc.fetch_1mo_prices_yf("AAA")
    assert len(result) == 1
    assert result.iloc[0]["Close"] == 5


def test_fetch_1mo_prices_yf_no_data(monkeypatch):
    class FakeTicker:
        def history(self, period="1mo"):
            return pd.DataFrame()

    monkeypatch.setattr(mc.yf, "Ticker", lambda s: FakeTicker())
    monkeypatch.setattr(mc.yf, "download", lambda *a, **k: pd.DataFrame())

    with pytest.raises(ValueError):
        mc.fetch_1mo_prices_yf("AAA")


def test_fetch_fin_stmt_from_yf_success(monkeypatch):
    class DF(pd.DataFrame):
        def __bool__(self):  # avoid ValueError on `or` check
            return True

    df = DF({"A": [1]})

    class FakeTicker:
        def __init__(self, d):
            self.financials = d

    monkeypatch.setattr(mc.yf, "Ticker", lambda s: FakeTicker(df))

    result = mc.fetch_fin_stmt_from_yf("AAA", "financials")
    assert not result.empty
    assert result.iloc[0]["A"] == 1


def test_fetch_fin_stmt_from_yf_error(monkeypatch):
    class FakeTicker:
        @property
        def financials(self):
            raise RuntimeError("fail")

    monkeypatch.setattr(mc.yf, "Ticker", lambda s: FakeTicker())

    result = mc.fetch_fin_stmt_from_yf("AAA", "financials")
    assert result.empty
