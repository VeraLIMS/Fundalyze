"""Edge-case tests for data.compare helpers."""
import pandas as pd
from data.compare import is_complete


ESSENTIAL_COLS = ["longName", "sector", "industry", "marketCap", "website"]

def test_is_complete_true():
    data = {c: [1] for c in ESSENTIAL_COLS}
    df = pd.DataFrame(data)
    assert is_complete(df)


def test_is_complete_missing_col():
    data = {c: [1] for c in ESSENTIAL_COLS[:-1]}
    df = pd.DataFrame(data)
    assert not is_complete(df)


def test_is_complete_empty():
    assert not is_complete(pd.DataFrame())
