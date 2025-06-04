from unittest.mock import MagicMock, patch

from modules.data.fetching import fetch_basic_stock_data


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

    with patch("modules.data.fetching.yf.Ticker") as mock_ticker_cls, \
         patch("modules.data.fetching.resolve_term", side_effect=lambda x: x):
        mock_ticker = MagicMock()
        mock_ticker.info = mock_info
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


def test_fetch_basic_stock_data_invalid():
    with patch("modules.data.fetching.yf.Ticker") as mock_ticker_cls, \
         patch("modules.data.fetching.resolve_term", side_effect=lambda x: x):
        mock_ticker = MagicMock()
        mock_ticker.info = {}
        mock_ticker_cls.return_value = mock_ticker

        import pytest
        with pytest.raises(ValueError):
            fetch_basic_stock_data("BAD")

