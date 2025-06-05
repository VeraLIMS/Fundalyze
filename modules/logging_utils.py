"""Utility for configuring a consistent logging setup."""

import logging
from pathlib import Path


def setup_logging(log_file: str = "fundalyze.log", level: int = logging.DEBUG) -> None:
    """Configure root logger to log to console and ``log_file``.

    Parameters
    ----------
    log_file:
        File path where logs will be written. Directory will be created if
        needed.
    level:
        Logging level for the root logger.
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
