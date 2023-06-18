"""Utilities for Sherlock's functioning."""

import logging
import sys

def get_logger(name) -> logging.Logger:
    """Returns a python Logger object."""
    # Initialize logger and set options/formats
    logger = logging.getLogger(name)
    # Set level
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    # Format string
    formatter = logging.Formatter("[%(asctime)s - %(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger