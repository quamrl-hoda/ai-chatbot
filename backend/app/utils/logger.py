"""
app/utils/logger.py – Centralised logging setup.
"""
import logging
import sys


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Returns a named logger configured with a consistent format.
    Call once per module: logger = get_logger(__name__)
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger
