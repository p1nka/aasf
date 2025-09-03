# aasf/logger_config.py

import logging
import sys


def setup_logging(log_level="INFO"):
    """Configures the root logger for the AASF application."""
    log_level = getattr(logging, log_level.upper(), logging.INFO)

    # Use a specific name for the logger to avoid interfering with other libraries
    logger = logging.getLogger("AASF")
    logger.setLevel(log_level)

    # Prevent adding handlers multiple times if the function is called again
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger