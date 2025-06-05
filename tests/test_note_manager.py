"""Tests for the Markdown note management system."""
import os
import tempfile

import importlib

from management.note_manager import note_manager


def test_slugify():
    assert note_manager.slugify("Hello World!") == "hello-world"


def test_parse_links():
    text = "See [[Note One]] and [[Note Two]] for details."
    assert note_manager.parse_links(text) == ["Note One", "Note Two"]


def test_create_and_read_note():
    with tempfile.TemporaryDirectory() as tmp:
        os.environ["NOTES_DIR"] = tmp
        importlib.reload(note_manager)
        note_manager.create_note("Test", "sample content")
        path = note_manager.get_note_path("Test")
        assert path.is_file()
        content = note_manager.read_note("Test")
        assert "sample content" in content
        del os.environ["NOTES_DIR"]
        importlib.reload(note_manager)

