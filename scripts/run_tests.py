#!/usr/bin/env python
"""Run each test file under the ``tests`` directory sequentially.

This script discovers all ``test_*.py`` files inside the repository's ``tests``
folder and executes them one by one using pytest in quiet mode. It is a simple
helper so you can run all tests automatically without typing the pytest command
manually.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    """Return parsed CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Run each test file under the tests directory sequentially",
        epilog="Example: python scripts/run_tests.py test_analytics*.py",
    )
    parser.add_argument(
        "pattern",
        nargs="?",
        default="test_*.py",
        help="Glob pattern to select test files (default: test_*.py)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    tests_dir = repo_root / "tests"
    test_files = sorted(tests_dir.glob(args.pattern))
    failures: list[str] = []

    for test_file in test_files:
        print(f"Running {test_file.name}")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", str(test_file)],
            check=False,
        )
        if result.returncode != 0:
            failures.append(test_file.name)

    if failures:
        print(f"\n{len(failures)} test files failed: {', '.join(failures)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
