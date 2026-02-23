# backend/modules/config_backup/utils.py

import os
import logging
import re
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
# RAW RECORDER
# -------------------------------------------------
class RawRecorder:
    def __init__(self, ip, protocol, debug_base_path: Path):
        tsf = datetime.now().strftime("%H.%M.%S")
        date = today_date()

        self.path = debug_base_path / date
        self.path.mkdir(parents=True, exist_ok=True)

        self.file = open(
            self.path / f"{ip}-{tsf}-{protocol}.raw",
            "w",
            encoding="utf-8",
            errors="ignore",
            buffering=1,
        )

        self._header(ip, protocol)

    def _header(self, ip, protocol):
        self.file.write("=" * 60 + "\n")
        self.file.write("RAW SESSION START\n")
        self.file.write(f"Protocol   : {protocol}\n")
        self.file.write(f"Destination: {ip}\n")
        self.file.write(f"Start Time : {now_timestamp()}\n")
        self.file.write("=" * 60 + "\n")

    def event(self, tag, text=""):
        line = f"[{now_timestamp()}] [{tag}] {text}".rstrip()
        self.file.write(line + "\n")

    def raw(self, data):
        if data:
            self.file.write(data)
            self.file.flush()

    def close(self, status):
        self.file.write("\n")
        self.file.write(f"[{now_timestamp()}] [SESSION_END] {status}\n")
        self.file.write("=" * 60 + "\n")
        self.file.close()


# -------------------------------------------------
# PROMPT HELPERS
# -------------------------------------------------
def load_prompt_patterns(path):
    patterns = []

    if not os.path.exists(path):
        raise FileNotFoundError(f"Prompt file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith("/") and line.endswith("/i"):
                patterns.append(re.compile(line[1:-2], re.I))
            elif line.startswith("/") and line.endswith("/"):
                patterns.append(re.compile(line[1:-1]))
            else:
                patterns.append(line.lower())

    return patterns


def match_prompt(data, patterns):
    data_l = data.lower()
    for p in patterns:
        if isinstance(p, re.Pattern):
            if p.search(data):
                return True, "REGEX"
        else:
            if p in data_l:
                return True, "TEXT"
    return False, None


# -------------------------------------------------
# CONFIG CLEANING
# -------------------------------------------------
def clean_config(raw):
    if not raw:
        return ""

    lines = raw.splitlines()
    cleaned = []

    skip_patterns = [
        r"^\s*terminal length\s*\d*",
        r"^terminal datadump",
        r"^show running-config",
        r"^More:",
        r"% Unrecognized command",
        r"^username:",
        r"^user name:",
        r"^password:",
        r"% Invalid",
        r"^\s*\^\s*",

    ]

    prompt_pattern = re.compile(r"^\S+[>#]")
    seen_prompt = False

    for line in lines:
        # Remove NUL characters
        line = line.replace("\x00", "")

        # Remove carriage returns
        line = line.replace("\r", "")

        # Remove ANSI escape sequences
        line = re.sub(r"\x1B\[[0-?]*[ -/]*[@-~]", "", line)

        # Strip leading/trailing whitespace
        line = line.strip()

        if not seen_prompt:
            if prompt_pattern.match(line):
                seen_prompt = True
            continue

        if any(re.search(p, line, re.I) for p in skip_patterns):
            continue

        if prompt_pattern.match(line):
            continue

        if line:
            cleaned.append(line)

    return "\n".join(cleaned).strip() + "\n"


# -------------------------------------------------
# HOSTNAME EXTRACTION
# -------------------------------------------------
def extract_hostname(raw, fallback):
    if not raw:
        return fallback
    m = re.search(r"^(\S+)[>#]", raw, re.MULTILINE)
    return m.group(1) if m else fallback
