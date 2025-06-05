"""Tests for term mapping utilities."""
from pathlib import Path
from modules.data.term_mapper import MAPPING_FILE, load_mapping


def test_mapping_file_location_and_load():
    repo_root = Path(__file__).resolve().parents[1]
    expected = repo_root / "config" / "term_mapping.json"
    assert MAPPING_FILE == expected
    mapping = load_mapping()
    assert "Technology" in mapping
