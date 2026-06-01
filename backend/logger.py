import logging
import os
from datetime import datetime

def setup_logger():
    os.makedirs("logs", exist_ok=True)
    formatter=logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)-25s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler = logging.FileHandler(
        f"logs/serendib_{datetime.now().strftime('%Y-%m-%d')}.log",
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

     # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Root logger
    logger = logging.getLogger("serendib")
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

logger= setup_logger()

