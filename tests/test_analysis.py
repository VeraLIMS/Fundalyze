import pandas as pd
from analytics import portfolio_summary, sector_counts
import pytest
from analytics import correlation_matrix


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


def test_sector_counts_basic():
    df = pd.DataFrame({"Sector": ["Tech", "Health", "Tech", None]})
    result = sector_counts(df)
    assert len(result) == 3
    assert result.iloc[0].tolist() == ["Tech", 2]
    assert result.iloc[1].tolist() == ["Health", 1]
    assert result.iloc[2].tolist() == ["Unknown", 1]


def test_sector_counts_no_sector_column():
    df = pd.DataFrame({"Ticker": ["A", "B"]})
    assert sector_counts(df).empty

def test_correlation_matrix_basic():
    df = pd.DataFrame({
        "A": [1, 2, 3],
        "B": [2, 4, 6],
        "Label": ["x", "y", "z"],
    })
    corr = correlation_matrix(df)
    assert list(corr.index) == ["A", "B"]
    assert corr.loc["A", "B"] == pytest.approx(1.0)


def test_correlation_matrix_insufficient_data():
    df = pd.DataFrame({"A": [1, 2, 3]})
    assert correlation_matrix(df).empty
