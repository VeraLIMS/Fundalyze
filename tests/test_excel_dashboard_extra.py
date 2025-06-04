import pytest
from pathlib import Path

from modules.generate_report.excel_dashboard import create_dashboard, show_dashboard_in_excel


def test_create_dashboard_missing_folder(tmp_path):
    missing = tmp_path / "nope"
    with pytest.raises(FileNotFoundError):
        create_dashboard(output_root=str(missing))


def test_show_dashboard_in_excel_missing_file(tmp_path):
    path = tmp_path / "dash.xlsx"
    with pytest.raises(FileNotFoundError):
        show_dashboard_in_excel(path)
