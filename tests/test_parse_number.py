import pandas as pd
from modules.utils import parse_number


def test_parse_number_numeric():
    assert parse_number(10) == 10


def test_parse_number_suffixes():
    assert parse_number("1.5B") == 1.5 * 1_000_000_000
    assert parse_number("2M") == 2 * 1_000_000
    assert parse_number("3k") == 3 * 1_000
    assert parse_number("100") == 100.0


def test_parse_number_invalid():
    assert parse_number("N/A") == "N/A"
    assert parse_number(None) is None
    assert parse_number(pd.NA) is pd.NA
