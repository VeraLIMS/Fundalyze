#!/usr/bin/env python3
"""Standalone launcher for the note manager utility."""

from modules.management.note_manager import run_note_manager


def main() -> None:
    """Launch the note manager."""
    run_note_manager()


if __name__ == "__main__":
    main()
