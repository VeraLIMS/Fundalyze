import pandas as pd
from unittest.mock import MagicMock

import modules.data.fetching as fetching
from analytics import portfolio_summary, sector_counts
import modules.management.portfolio_manager.portfolio_manager as pm


def test_fetch_to_analysis_integration(monkeypatch):
    info_map = {
        "AAA": {
            "longName": "Alpha Inc",
            "sector": "Tech",
            "industry": "Software",
            "currentPrice": 10.0,
            "marketCap": 100,
            "trailingPE": 20.0,
            "dividendYield": 0.01,
        },
        "BBB": {
            "longName": "Beta Corp",
            "sector": "Health",
            "industry": "Biotech",
            "currentPrice": 20.0,
            "marketCap": 200,
            "trailingPE": 25.0,
            "dividendYield": 0.02,
        },
    }

    def mock_ticker(symbol):
        mock = MagicMock()
        mock.get_info.return_value = info_map.get(symbol, {})
        return mock

    monkeypatch.setattr(fetching.yf, "Ticker", mock_ticker)
    monkeypatch.setattr(fetching, "resolve_term", lambda x: x)

    row_a = fetching.fetch_basic_stock_data("AAA")
    row_b = fetching.fetch_basic_stock_data("BBB")
    df = pd.DataFrame([row_a, row_b])

    summary = portfolio_summary(df)
    counts = sector_counts(df)

    assert summary.loc["mean", "Current Price"] == 15.0
    assert summary.loc["max", "Market Cap"] == 200
    assert counts.sort_values("Sector").reset_index(drop=True).to_dict(orient="records") == [
        {"Sector": "Health", "Count": 1},
        {"Sector": "Tech", "Count": 1},
    ]


def test_portfolio_manager_add_tickers(monkeypatch):
    info_map = {
        "AAA": {
            "longName": "Alpha Inc",
            "sector": "Tech",
            "industry": "Software",
            "currentPrice": 10.0,
            "marketCap": 100,
            "trailingPE": 20.0,
            "dividendYield": 0.01,
        },
        "BBB": {
            "longName": "Beta Corp",
            "sector": "Health",
            "industry": "Biotech",
            "currentPrice": 20.0,
            "marketCap": 200,
            "trailingPE": 25.0,
            "dividendYield": 0.02,
        },
    }

    def mock_ticker(symbol):
        mock = MagicMock()
        mock.get_info.return_value = info_map.get(symbol, {})
        return mock

    monkeypatch.setattr(fetching.yf, "Ticker", mock_ticker)
    monkeypatch.setattr(fetching, "resolve_term", lambda x: x)

    # ensure portfolio manager uses the real fetch_basic_stock_data
    monkeypatch.setattr(pm, "fetch_from_yfinance", fetching.fetch_basic_stock_data)

    inputs = iter([
        "AAA,BBB",  # ticker list
        "y",        # confirm AAA data
        "y",        # confirm BBB data
    ])
    monkeypatch.setattr("builtins.input", lambda *_args: next(inputs))

    df = pd.DataFrame(columns=pm.COLUMNS)
    result = pm.add_tickers(df)

    assert set(result["Ticker"]) == {"AAA", "BBB"}
    counts = sector_counts(result)
    assert set(counts["Sector"]) == {"Tech", "Health"}
