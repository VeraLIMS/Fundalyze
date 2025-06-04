import pandas as pd
from modules.interface import print_table


def test_print_table_empty(capsys):
    print_table(pd.DataFrame())
    captured = capsys.readouterr().out.strip()
    assert captured == "(no data)"


def test_print_table_non_empty(capsys):
    df = pd.DataFrame({"A": [1]})
    print_table(df)
    out = capsys.readouterr().out
    assert "A" in out and "1" in out
