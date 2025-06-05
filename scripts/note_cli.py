#!/usr/bin/env python3
"""Standalone launcher for the note manager utility."""

import argparse
import os
import sys

SCRIPT_DIR = os.path.dirname(__file__)
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from modules.management.note_manager import run_note_manager


def parse_args() -> argparse.Namespace:
    """Return parsed CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Launch the Fundalyze note manager"
    )
    return parser.parse_args()


def main() -> None:
    """Launch the note manager."""
    parse_args()  # handles --help
    run_note_manager()


if __name__ == "__main__":
    main()
