"""Extra cases for Excel dashboard helpers."""
import pytest
pytest.skip("Deprecated after Directus migration", allow_module_level=True)
import pytest
import pandas as pd
from modules.generate_report.excel_dashboard import (
    create_dashboard,
    show_dashboard_in_excel,
)


def test_create_dashboard_missing_folder(tmp_path):
    missing = tmp_path / "nope"
    with pytest.raises(FileNotFoundError):
        create_dashboard(output_root=str(missing))


def test_show_dashboard_in_excel_missing_file(tmp_path):
    path = tmp_path / "dash.xlsx"
    with pytest.raises(FileNotFoundError):
        show_dashboard_in_excel(path)

def test_create_dashboard_with_progress(tmp_path):
    ticker_dir = tmp_path / "AAA"
    ticker_dir.mkdir()
    pd.DataFrame({"symbol": ["AAA"]}).to_csv(ticker_dir / "profile.csv", index=False)
    pd.DataFrame({"Date": pd.date_range("2023-01-01", periods=1)}).to_csv(
        ticker_dir / "1mo_prices.csv", index=False
    )
    path = create_dashboard(output_root=str(tmp_path), progress=True)
    assert path.is_file()
