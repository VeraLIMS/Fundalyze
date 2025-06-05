from __future__ import annotations

"""Helper utilities for working with Excel files."""

import pandas as pd


def col_to_letter(idx: int) -> str:
    """Return Excel-style column letters (0-based)."""
    letters = ""
    while idx >= 0:
        idx, rem = divmod(idx, 26)
        letters = chr(65 + rem) + letters
        idx -= 1
    return letters


def write_table(
    writer: pd.ExcelWriter,
    df: pd.DataFrame,
    sheet_name: str,
    table_name: str,
    *,
    style: str = "Table Style Medium 2",
) -> None:
    """Write ``df`` to ``sheet_name`` and convert it to a formatted table."""
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    worksheet = writer.sheets[sheet_name]

    nrows, ncols = df.shape
    table_range = f"A1:{col_to_letter(ncols - 1)}{nrows + 1}"
    worksheet.add_table(
        table_range,
        {
            "name": table_name,
            "columns": [{"header": col} for col in df.columns],
            "autofilter": True,
            "style": style,
        },
    )

