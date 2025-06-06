"""Convenience imports for utility functions.

These are small helpers used throughout Fundalyze. Importing from the package
provides shorter names::

    from modules import utils
    df = utils.read_csv_if_exists(Path("prices.csv"))
"""

from .data_utils import (
    strip_timezones,
    ensure_period_column,
    read_csv_if_exists,
    read_json_if_exists,
    parse_number,
    parse_human_number,
)
from .math_utils import moving_average, percentage_change
from .progress_utils import progress_iter
from .openbb_utils import get_openbb

__all__ = [
    "strip_timezones",
    "ensure_period_column",
    "read_csv_if_exists",
    "read_json_if_exists",
    "parse_number",
    "parse_human_number",
    "moving_average",
    "percentage_change",
    "progress_iter",
    "get_openbb",
]
