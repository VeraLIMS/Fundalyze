"""Additional tests for interface presentation functions."""
import pandas as pd
from modules.interface import (
    INVALID_CHOICE_MSG,
    input_or_cancel,
    print_header,
    print_invalid_choice,
    print_menu,
    print_table,
)


def test_print_table_empty(capsys):
    print_table(pd.DataFrame())
    captured = capsys.readouterr().out.strip()
    assert captured == "(no data)"


def test_print_table_non_empty(capsys):
    df = pd.DataFrame({"A": [1]})
    print_table(df)
    out = capsys.readouterr().out
    assert "A" in out and "1" in out


def test_print_header_formats_title(capsys):
    print_header("Hello")
    captured = capsys.readouterr().out.strip()
    assert captured == "=== Hello ==="


def test_print_invalid_choice_message(capsys):
    print_invalid_choice()
    captured = capsys.readouterr().out.strip()
    assert captured == INVALID_CHOICE_MSG.strip()


def test_input_or_cancel_value(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "  data  ")
    result = input_or_cancel("Prompt")
    assert result == "data"


def test_input_or_cancel_empty(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "   ")
    result = input_or_cancel("Prompt")
    assert result == ""


def test_print_menu_lists_options(capsys):
    print_menu(["one", "two"])
    lines = capsys.readouterr().out.strip().splitlines()
    assert lines == ["1) one", "2) two"]
