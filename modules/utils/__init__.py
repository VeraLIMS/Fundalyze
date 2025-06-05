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
)
from .excel_utils import col_to_letter, write_table
from .math_utils import moving_average, percentage_change
from .progress_utils import progress_iter

__all__ = [
    "strip_timezones",
    "ensure_period_column",
    "read_csv_if_exists",
    "read_json_if_exists",
    "col_to_letter",
    "write_table",
    "moving_average",
    "percentage_change",
    "progress_iter",
]
