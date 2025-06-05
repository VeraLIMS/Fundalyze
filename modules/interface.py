from __future__ import annotations

import pandas as pd
from tabulate import tabulate

INVALID_CHOICE_MSG = "Invalid choice. Please select a valid option.\n"


def print_table(df: pd.DataFrame, *, showindex: bool = False) -> None:
    """Pretty-print a DataFrame using :mod:`tabulate`."""
    if df is None or df.empty:
        print("(no data)")
        return
    print(tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=showindex))


def print_invalid_choice() -> None:
    """Standard message for invalid menu selections."""
    print(INVALID_CHOICE_MSG)
