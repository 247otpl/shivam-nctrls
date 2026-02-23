# backend/modules/command_executor/utils.py

import os
import logging
from datetime import datetime
from pathlib import Path

DATE_FORMAT = "%d-%m-%Y"
DATETIME_FORMAT = "%d-%m-%Y %H:%M:%S"


# -------------------------------------------------
# DATE HELPERS
# -------------------------------------------------
def today_date():
    return datetime.now().strftime(DATE_FORMAT)


def now_timestamp():
    return datetime.now().strftime(DATETIME_FORMAT)


# -------------------------------------------------
# AUTH LOGGING
# -------------------------------------------------
def setup_logging(log_file: Path):
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("AUTH")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s %(message)s",
            datefmt=DATETIME_FORMAT,
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


# -------------------------------------------------
# COMMAND LOADER
# -------------------------------------------------
def load_commands(path: Path):
    commands = []

    if not path.exists():
        raise FileNotFoundError(f"Commands file not found: {path}")

    with open(path, encoding="utf-8") as f:
        for line in f:
            cmd = line.rstrip()
            if not cmd:
                continue

            if cmd.startswith(("!", "#", "//")):
                commands.append(("SKIP", cmd))
            else:
                commands.append(("EXEC", cmd))

    return commands
