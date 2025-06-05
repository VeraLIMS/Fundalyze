import pandas as pd
import pytest
from generate_report.excel_dashboard import (
    _safe_concat_normal,
    _transpose_financials,
    _strip_timezones,
)
from modules.utils.excel_utils import col_to_letter


def test_col_to_letter_basic():
    assert col_to_letter(0) == "A"
    assert col_to_letter(1) == "B"
    assert col_to_letter(25) == "Z"
    assert col_to_letter(26) == "AA"
    assert col_to_letter(51) == "AZ"
    assert col_to_letter(52) == "BA"


def test_col_to_letter_negative():
    with pytest.raises(ValueError):
        col_to_letter(-1)


def test_safe_concat_normal():
    dfs = {
        "AAA": pd.DataFrame({"X": [1], "Y": [2]}),
        "BBB": pd.DataFrame({"X": [3], "Y": [4]}),
    }
    result = _safe_concat_normal(dfs)
    assert list(result.columns) == ["Ticker", "X", "Y"]
    assert result.iloc[0].tolist() == ["AAA", 1, 2]
    assert result.iloc[1].tolist() == ["BBB", 3, 4]


def test_safe_concat_normal_empty():
    result = _safe_concat_normal({})
    assert result.empty


def test_transpose_financials():
    dfs = {
        "AAA": pd.DataFrame({
            "Period": ["2023-06", "2023-03"],
            "Revenue": [10, 20],
            "EPS": [1, 2],
        }),
        "BBB": pd.DataFrame({
            "Period": ["2023-06"],
            "Revenue": [30],
            "EPS": [3],
        }),
    }
    result = _transpose_financials(dfs)
    expected_columns = ["Ticker", "Metric", "2023-06", "2023-03"]
    assert list(result.columns) == expected_columns
    # There should be 3 metrics total: 2 for AAA and 1 for BBB (since BBB only has one period)
    assert len(result) == 4
    # Check first ticker block
    first_block = result.iloc[0:2]
    assert first_block.iloc[0].tolist() == ["AAA", "Revenue", 10, 20]
    assert first_block.iloc[1].tolist() == ["AAA", "EPS", 1, 2]
    # Check second ticker block
    second_block = result.iloc[2:4]
    assert second_block.iloc[0, 0] == "BBB"
    assert second_block.iloc[0, 1] == "Revenue"
    assert second_block.iloc[0, 2] == 30
    assert pd.isna(second_block.iloc[0, 3])
    assert second_block.iloc[1, 0] == "BBB"
    assert second_block.iloc[1, 1] == "EPS"
    assert second_block.iloc[1, 2] == 3
    assert pd.isna(second_block.iloc[1, 3])


def test_transpose_financials_index_input():
    dfs = {
        "AAA": pd.DataFrame({"Revenue": [10, 20]}, index=["2023-06", "2023-03"]),
        "BBB": pd.DataFrame({"Revenue": [30]}, index=["2023-06"]),
    }
    result = _transpose_financials(dfs)
    assert list(result.columns) == ["Ticker", "Metric", "2023-06", "2023-03"]
    assert len(result) == 2
    assert result.iloc[0].tolist() == ["AAA", "Revenue", 10, 20]
    second = result.iloc[1].tolist()
    assert second[0] == "BBB"
    assert second[1] == "Revenue"
    assert second[2] == 30
    assert pd.isna(second[3])


def test_strip_timezones_removes_tz():
    idx = pd.DatetimeIndex(["2024-01-01"], tz="UTC")
    df = pd.DataFrame({"val": [1], "ts": pd.Series([pd.Timestamp("2024-01-02", tz="UTC")])}, index=idx)
    result = _strip_timezones(df.copy())
    assert result.index.tz is None
    assert result["ts"].dtype == "datetime64[ns]"
