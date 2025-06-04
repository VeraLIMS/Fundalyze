import pandas as pd
from analytics import portfolio_summary


def test_portfolio_summary_numeric_columns():
    df = pd.DataFrame({
        "Ticker": ["A", "B"],
        "Price": [10.0, 20.0],
        "Volume": [100, 150]
    })
    summary = portfolio_summary(df)
    assert list(summary.index) == ["mean", "min", "max"]
    assert list(summary.columns) == ["Price", "Volume"]
    assert summary.loc["mean", "Price"] == 15.0
    assert summary.loc["min", "Volume"] == 100
    assert summary.loc["max", "Volume"] == 150


def test_portfolio_summary_empty():
    assert portfolio_summary(pd.DataFrame()).empty
