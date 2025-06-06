"""Tests for yfinance fallback data retrieval."""
import pytest
pytest.skip("Deprecated after Directus migration", allow_module_level=True)
import json
import pandas as pd
from unittest.mock import MagicMock

import modules.generate_report.fallback_data as fb


def test_fetch_profile_from_fmp_success(monkeypatch):
    resp = MagicMock()
    resp.json.return_value = [{
        "symbol": "AAA",
        "companyName": "Alpha Inc",
        "sector": "Tech",
        "industry": "Software",
        "mktCap": 100,
        "website": "example.com",
    }]
    resp.raise_for_status.return_value = None
    monkeypatch.setattr(fb.requests, "get", lambda url, **kwargs: resp)

    df = fb.fetch_profile_from_fmp("AAA")
    assert df.iloc[0]["sector"] == "Tech"
    assert df.iloc[0]["website"] == "example.com"


def test_fetch_profile_from_fmp_no_data(monkeypatch):
    resp = MagicMock()
    resp.json.return_value = []
    resp.raise_for_status.return_value = None
    monkeypatch.setattr(fb.requests, "get", lambda url, **kwargs: resp)

    import pytest
    with pytest.raises(ValueError):
        fb.fetch_profile_from_fmp("AAA")


def test_fetch_fmp_statement(monkeypatch):
    resp = MagicMock()
    resp.json.return_value = [{"date": "2023", "Revenue": 5}]
    resp.raise_for_status.return_value = None
    monkeypatch.setattr(fb.requests, "get", lambda url, **kwargs: resp)

    df = fb.fetch_fmp_statement("AAA", "income-statement", "annual")
    assert df.index.name == "date"
    assert df.loc["2023", "Revenue"] == 5


def test_fetch_1mo_prices_fmp(monkeypatch):
    resp = MagicMock()
    resp.json.return_value = {
        "historical": [
            {
                "date": "2023-01-02",
                "open": 1,
                "high": 2,
                "low": 0.5,
                "close": 1.5,
                "adjClose": 1.5,
                "volume": 100,
            }
        ]
    }
    resp.raise_for_status.return_value = None
    monkeypatch.setattr(fb.requests, "get", lambda url, **kwargs: resp)

    df = fb.fetch_1mo_prices_fmp("AAA")
    assert list(df.columns) == [
        "Date",
        "Open",
        "High",
        "Low",
        "Close",
        "Adj Close",
        "Volume",
    ]
    assert len(df) == 1


def test_fetch_1mo_prices_fmp_no_data(monkeypatch):
    resp = MagicMock()
    resp.json.return_value = {"historical": []}
    resp.raise_for_status.return_value = None
    monkeypatch.setattr(fb.requests, "get", lambda url, **kwargs: resp)

    import pytest

    with pytest.raises(ValueError):
        fb.fetch_1mo_prices_fmp("AAA")


def test_enrich_ticker_folder_updates_files(tmp_path, monkeypatch):
    ticker_dir = tmp_path / "AAA"
    ticker_dir.mkdir()
    meta = {
        "files": {
            "profile.csv": {"source": "ERROR", "source_url": "", "fetched_at": "old"},
            "1mo_prices.csv": {"source": "ERROR", "source_url": "", "fetched_at": "old"},
        }
    }
    (ticker_dir / "metadata.json").write_text(json.dumps(meta))

    profile_df = pd.DataFrame({
        "symbol": ["AAA"],
        "longName": ["Alpha"],
        "sector": ["Tech"],
        "industry": ["Software"],
        "marketCap": [10],
        "website": ["a.com"],
    })
    monkeypatch.setattr(fb, "fetch_profile_from_fmp", lambda s: profile_df)

    price_df = pd.DataFrame({
        "Open": [1],
        "High": [1],
        "Low": [1],
        "Close": [1],
        "Adj Close": [1],
        "Volume": [10],
    }, index=pd.DatetimeIndex(["2024-01-01"], name="Date"))

    class FakeTicker:
        def history(self, period="1mo"):
            return price_df
        info = {}

    monkeypatch.setattr(fb.yf, "Ticker", lambda s: FakeTicker())
    monkeypatch.setattr(fb, "iso_timestamp_utc", lambda: "2024-01-02T00:00:00Z")

    fb.enrich_ticker_folder(ticker_dir)

    updated = json.loads((ticker_dir / "metadata.json").read_text())
    assert updated["files"]["profile.csv"]["source"] == "FMP (profile)"
    assert updated["files"]["1mo_prices.csv"]["source"] == "yfinance.history"
    assert (ticker_dir / "profile.csv").is_file()
    assert (ticker_dir / "1mo_prices.csv").is_file()
