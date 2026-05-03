"""
core/logger.py
--------------
Structured logging setup for the SQL Transformation Framework.
Outputs human-readable logs to console and optionally to a log file.
"""

import logging
import sys
from pathlib import Path


_FORMATTER = logging.Formatter(
    fmt="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def get_logger(name: str, log_file: str = None) -> logging.Logger:
    """
    Get a configured logger instance.

    Args:
        name:     Logger name (usually the calling class or module).
        log_file: Optional path to write logs to a file as well.

    Returns:
        A configured logging.Logger instance.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # Already configured

    logger.setLevel(logging.DEBUG)

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(_FORMATTER)
    logger.addHandler(ch)

    # Optional file handler
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(_FORMATTER)
        logger.addHandler(fh)

    return logger
