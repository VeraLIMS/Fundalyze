"""Regression tests for diff_dict helper."""
from data.compare import diff_dict


def test_diff_dict():
    d1 = {"a": 1, "b": 2}
    d2 = {"a": 1, "b": 3, "c": 4}
    assert diff_dict(d1, d2) == {"b": (2, 3), "c": (None, 4)}


def test_diff_dict_empty():
    assert diff_dict({}, {}) == {}
