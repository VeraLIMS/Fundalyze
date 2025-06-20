"""Tests for data utility edge scenarios."""
import json
import pandas as pd
from modules.utils.data_utils import (
    ensure_period_column,
    read_csv_if_exists,
    read_json_if_exists,
    strip_timezones,
    write_dataframe,
)


def test_ensure_period_column_existing():
    df = pd.DataFrame({'Period': ['2020-01', '2020-02'], 'A': [1, 2]})
    result = ensure_period_column(df.copy())
    assert list(result.columns) == ['Period', 'A']
    assert result.equals(df)


def test_ensure_period_column_from_index():
    df = pd.DataFrame({'A': [1, 2]}, index=['2020-01', '2020-02'])
    result = ensure_period_column(df)
    assert 'Period' in result.columns
    assert result['Period'].tolist() == ['2020-01', '2020-02']


def test_read_csv_if_exists_missing(tmp_path):
    path = tmp_path / 'missing.csv'
    assert read_csv_if_exists(path) is None


def test_read_csv_if_exists_bad_csv(tmp_path):
    path = tmp_path / 'bad.csv'
    path.write_text('not,csv\n"unterminated')
    assert read_csv_if_exists(path) is None


def test_read_csv_if_exists_success(tmp_path):
    path = tmp_path / 'good.csv'
    pd.DataFrame({'A': [1]}).to_csv(path, index=False)
    result = read_csv_if_exists(path)
    assert result is not None
    assert result['A'].tolist() == [1]


def test_read_json_if_exists(tmp_path):
    path = tmp_path / 'data.json'
    data = {"a": 1, "b": 2}
    path.write_text('{"a": 1, "b": 2}', encoding='utf-8')
    result = read_json_if_exists(path)
    assert result == data


def test_read_json_if_exists_missing(tmp_path):
    path = tmp_path / 'missing.json'
    assert read_json_if_exists(path) is None


def test_strip_timezones():
    idx = pd.date_range('2020-01-01', periods=2, tz='UTC')
    df = pd.DataFrame({'A': pd.date_range('2020-01-01', periods=2, tz='US/Eastern')}, index=idx)
    result = strip_timezones(df)
    assert result.index.tz is None
    assert result['A'].dt.tz is None


def test_write_dataframe_csv_and_json(tmp_path):
    df = pd.DataFrame({'A': [1]})
    path = tmp_path / 'out.csv'
    write_dataframe(df, path, write_csv=True, write_json=True)
    assert path.is_file()
    csv_read = pd.read_csv(path)
    assert csv_read.equals(df)
    json_data = json.loads(path.with_suffix('.json').read_text())
    assert json_data[0]['A'] == 1
