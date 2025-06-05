 codex/create-comprehensive-documentation-for-fundalyze
"""Logging configuration helpers."""

=======
 codex/create-documentation-for-tests-module
"""Central logging configuration helpers."""
=======
 codex/document-logging_utils.py-usage
 codex/document-logging_utils.py-usage
"""Simple logging configuration helper.

Use :func:`setup_logging` at application startup to create ``fundalyze.log``
and enable console output.  Log records use the format::
=======
 codex/document-logs-and-logging-policy
"""Shared logging helpers used across Fundalyze utilities.

The :func:`setup_logging` function configures the root ``logging`` package to
write messages both to the console and to ``fundalyze.log`` under the project
``logs/`` directory.  Each log entry uses the format
``YYYY-MM-DD HH:MM:SS [LEVEL] logger_name: message`` and is written
immediately through Python's standard logging handlers.

No rotation is currently configured; the log file will grow until manually
deleted or rotated by external tooling.
"""
 main
=======
"""Utility for configuring a consistent logging setup."""
 main

 main
 main
import logging
from pathlib import Path
 main

    YYYY-MM-DD HH:MM:SS [LEVEL] logger: message
"""

import logging
from pathlib import Path
def setup_logging(log_file: str = "fundalyze.log", level: int = logging.DEBUG) -> None:
    """Configure the root logger and open ``log_file``.

    Parameters
    ----------
    log_file:
        File path where logs will be written. Directory will be created if
        needed.
    level:
        Logging level for the root logger.

 codex/document-logging_utils.py-usage
    Example
    -------
    >>> from modules.logging_utils import setup_logging
    >>> setup_logging("logs/fundalyze.log")
=======
    Notes
    -----
    ``logging`` handles flushes automatically when the program exits or handlers
    are closed, so this function does not need to call ``flush()`` manually.
 main
    """
    path = Path(log_file)
    path.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logging.basicConfig(level=level, handlers=[file_handler, console_handler])
