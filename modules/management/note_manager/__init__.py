 codex/document-cli-management-tools-and-helpers
"""Public interface for the Markdown note manager CLI."""
=======
"""Public API for the note management utilities."""
 main

from .note_manager import (
    create_note,
    get_note_path,
    list_notes,
    parse_links,
    read_note,
    run_note_manager,
    slugify,
)

__all__ = [
    "create_note",
    "get_note_path",
    "list_notes",
    "parse_links",
    "read_note",
    "run_note_manager",
    "slugify",
]
