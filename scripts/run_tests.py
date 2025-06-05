#!/usr/bin/env python
"""Run each test file under the ``tests`` directory sequentially.

This script discovers all ``test_*.py`` files inside the repository's ``tests``
folder and executes them one by one using pytest in quiet mode. It is a simple
helper so you can run all tests automatically without typing the pytest command
manually.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    tests_dir = repo_root / "tests"
    test_files = sorted(tests_dir.glob("test_*.py"))
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
