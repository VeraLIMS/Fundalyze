from unittest.mock import MagicMock, patch

from modules.data.fetching import fetch_basic_stock_data, fetch_basic_stock_data_batch


def test_fetch_basic_stock_data_basic():
    mock_info = {
        "longName": "Acme Corp",
        "sector": "Tech",
        "industry": "Software",
        "currentPrice": 100.0,
        "marketCap": 2000000,
        "trailingPE": 15.0,
        "dividendYield": 0.01,
    }

    with patch("modules.data.fetching.yf.Ticker") as mock_ticker_cls, patch(
        "modules.data.fetching.resolve_term", side_effect=lambda x: x
    ):
        mock_ticker = MagicMock()
        mock_ticker.get_info.return_value = mock_info
        mock_ticker_cls.return_value = mock_ticker

        result = fetch_basic_stock_data("ACME")

    expected = {
        "Ticker": "ACME",
        "Name": "Acme Corp",
        "Sector": "Tech",
        "Industry": "Software",
        "Current Price": 100.0,
        "Market Cap": 2000000,
        "PE Ratio": 15.0,
        "Dividend Yield": 0.01,
    }
    assert result == expected


def test_fetch_basic_stock_data_invalid_no_fallback():
    with patch("modules.data.fetching.yf.Ticker") as mock_ticker_cls, patch(
        "modules.data.fetching.resolve_term", side_effect=lambda x: x
    ):
        mock_ticker = MagicMock()
        mock_ticker.get_info.return_value = {}
        mock_ticker_cls.return_value = mock_ticker

        import pytest

        with pytest.raises(ValueError):
            fetch_basic_stock_data("BAD", fallback=False)


def test_fetch_basic_stock_data_fmp_fallback():
    mock_fmp_data = [
        {
            "symbol": "ACME",
            "companyName": "Acme Corp",
            "sector": "Tech",
            "industry": "Software",
            "price": 50.0,
            "mktCap": 1000000,
            "pe": 12.0,
            "lastDiv": 0.02,
        }
    ]

    with patch("modules.data.fetching.yf.Ticker") as mock_ticker_cls, patch(
        "modules.data.fetching.requests.get"
    ) as mock_get, patch("modules.data.fetching.resolve_term", side_effect=lambda x: x):
        mock_ticker = MagicMock()
        mock_ticker.get_info.return_value = {}
        mock_ticker_cls.return_value = mock_ticker

        mock_resp = MagicMock()
        mock_resp.json.return_value = mock_fmp_data
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        result = fetch_basic_stock_data("ACME")

    expected = {
        "Ticker": "ACME",
        "Name": "Acme Corp",
        "Sector": "Tech",
        "Industry": "Software",
        "Current Price": 50.0,
        "Market Cap": 1000000,
        "PE Ratio": 12.0,
        "Dividend Yield": 0.02,
    }
    assert result == expected


def test_fetch_basic_stock_data_provider_yf(monkeypatch):
    mock_info = {
        "longName": "Acme Corp",
        "sector": "Tech",
        "industry": "Software",
        "currentPrice": 100.0,
        "marketCap": 2000000,
        "trailingPE": 15.0,
        "dividendYield": 0.01,
    }

    class FakeTicker:
        def get_info(self):
            return mock_info

    monkeypatch.setattr("modules.data.fetching.yf.Ticker", lambda t: FakeTicker())
    monkeypatch.setattr("modules.data.fetching.resolve_term", lambda x: x)

    result = fetch_basic_stock_data("ACME", provider="yf")
    assert result["Name"] == "Acme Corp"


def test_fetch_basic_stock_data_provider_fmp(monkeypatch):
    mock_resp = MagicMock()
    mock_resp.json.return_value = [
        {
            "symbol": "ACME",
            "companyName": "Acme Corp",
            "sector": "Tech",
            "industry": "Software",
            "price": 50.0,
            "mktCap": 1000000,
            "pe": 12.0,
            "lastDiv": 0.02,
        }
    ]
    mock_resp.raise_for_status.return_value = None
    monkeypatch.setattr("modules.data.fetching.requests.get", lambda *a, **k: mock_resp)
    monkeypatch.setattr("modules.data.fetching.resolve_term", lambda x: x)

    result = fetch_basic_stock_data("ACME", provider="fmp")
    assert result["PE Ratio"] == 12.0


def test_fetch_basic_stock_data_provider_yf_failure(monkeypatch):
    class FakeTicker:
        def get_info(self):
            return {}

    monkeypatch.setattr("modules.data.fetching.yf.Ticker", lambda t: FakeTicker())
    monkeypatch.setattr("modules.data.fetching.resolve_term", lambda x: x)
    import pytest

    with pytest.raises(ValueError):
        fetch_basic_stock_data("BAD", provider="yf")


def test_fetch_basic_stock_data_batch(monkeypatch):
    data = {
        "AAA": {
            "longName": "Alpha",
            "sector": "Tech",
            "industry": "Software",
            "currentPrice": 1.0,
            "marketCap": 10,
            "trailingPE": 5.0,
            "dividendYield": 0.01,
        },
        "BBB": {
            "longName": "Beta",
            "sector": "Health",
            "industry": "Biotech",
            "currentPrice": 2.0,
            "marketCap": 20,
            "trailingPE": 6.0,
            "dividendYield": 0.02,
        },
    }

    class FakeTicker:
        def __init__(self, symbol):
            self.symbol = symbol

        def get_info(self):
            return data.get(self.symbol, {})

    monkeypatch.setattr("modules.data.fetching.yf.Ticker", lambda s: FakeTicker(s))
    monkeypatch.setattr("modules.data.fetching.resolve_term", lambda x: x)

    df = fetch_basic_stock_data_batch(["AAA", "BBB"], progress=True, dedup=True)
    assert list(df["Ticker"]) == ["AAA", "BBB"]
    assert df.loc[0, "Market Cap"] == 10


def test_fetch_basic_stock_data_invalid_provider():
    import pytest

    with pytest.raises(ValueError):
        fetch_basic_stock_data("AAA", provider="unknown")


def test_fetch_basic_stock_data_batch_empty():
    df = fetch_basic_stock_data_batch([], progress=True)
    # Should return DataFrame with BASIC_FIELDS columns but no rows
    assert df.empty


def test_fetch_basic_stock_data_batch_dedup(monkeypatch):
    data = {
        "AAA": {
            "longName": "Alpha",
            "sector": "Tech",
            "industry": "Software",
            "currentPrice": 1.0,
            "marketCap": 10,
            "trailingPE": 5.0,
            "dividendYield": 0.01,
        }
    }

    class FakeTicker:
        def __init__(self, symbol):
            self.symbol = symbol

        def get_info(self):
            return data.get(self.symbol, {})

    monkeypatch.setattr("modules.data.fetching.yf.Ticker", lambda s: FakeTicker(s))
    monkeypatch.setattr("modules.data.fetching.resolve_term", lambda x: x)

    df = fetch_basic_stock_data_batch(["AAA", "AAA"], dedup=True)
    assert len(df) == 1
