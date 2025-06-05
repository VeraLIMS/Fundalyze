"""Tests for progress indicator helper."""
from modules.utils.progress_utils import progress_iter


def test_progress_iter_basic():
    values = [1, 2, 3]
    result = list(progress_iter(values, description="test"))
    assert result == values
