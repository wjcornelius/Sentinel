# -*- coding: utf-8 -*-
"""
Logging configuration for Sentinel.

Provides centralized logging setup with file and console handlers.
"""

import logging
import os
from datetime import datetime
from pathlib import Path

LOG_DIR = "logs"


def setup_logging():
    """
    Configure logging to both file and console with appropriate levels.

    File logs capture DEBUG and above for detailed troubleshooting.
    Console logs show WARNING and above to keep output clean.

    Returns:
        str: Path to the log file created for this session
    """
    Path(LOG_DIR).mkdir(exist_ok=True)

    log_filename = os.path.join(
        LOG_DIR,
        f"sentinel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File handler - detailed logging
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console handler - info and above (keeps console clean)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)

    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Clear any existing handlers to avoid duplicates
    logger.handlers.clear()

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logging.info("="*80)
    logging.info("Sentinel logging initialized")
    logging.info(f"Log file: {log_filename}")
    logging.info("="*80)

    return log_filename
