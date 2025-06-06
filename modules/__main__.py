"""Fundalyze command line entry point.

Running ``python -m modules`` launches the same interactive menu as
``python scripts/main.py``. This small wrapper allows the application to be
invoked as a package without relying on the scripts directory.
"""
from scripts.main import main

if __name__ == "__main__":
    main()
