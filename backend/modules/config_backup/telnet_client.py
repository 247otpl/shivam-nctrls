# backend/modules/config_backup/telnet_client.py

import telnetlib
import time
import re

from backend.modules.config_backup.settings import SHOW_CMD, ENABLE_PASSWORD
from backend.modules.config_backup.utils import (
    RawRecorder,
    load_prompt_patterns,
    match_prompt,
)

LOGIN_TIMEOUT = 25
IDLE_TIMEOUT = 8

CLI_PROMPT = re.compile(r"\S+[>#]\s*$")


def run_telnet(ip, port, username, password, debug_base_path):

    recorder = RawRecorder(ip, "TELNET", debug_base_path)
    raw = ""
    status = "UNKNOWN"

    user_prompts = load_prompt_patterns("prompts/login_username.txt")
    pass_prompts = load_prompt_patterns("prompts/login_password.txt")

    try:
        recorder.event("CONNECT", "Telnet session starting")

        tn = telnetlib.Telnet(ip, port, timeout=15)

        state = "WAIT_USERNAME"
        deadline = time.time() + LOGIN_TIMEOUT
        last_rx = time.time()

        def read():
            nonlocal raw, last_rx
            data = tn.read_very_eager().decode(errors="ignore")
            if data:
                recorder.raw(data)
                raw += data
                last_rx = time.time()
            return data

        def wait_for_prompt(timeout=15):
            end = time.time() + timeout
            while time.time() < end:
                data = read()
                if data and CLI_PROMPT.search(data):
                    return True
                time.sleep(0.2)
            return False

        # ------------------------------
        # LOGIN STATE MACHINE
        # ------------------------------
        while True:
            if time.time() > deadline:
                raise TimeoutError("Login prompt timeout")

            data = read()
            if not data:
                time.sleep(0.2)
                continue

            if state == "WAIT_USERNAME":
                matched, _ = match_prompt(data, user_prompts)
                if matched:
                    recorder.event("SEND", "USERNAME")
                    tn.write(username.encode() + b"\n")
                    state = "WAIT_PASSWORD"

            elif state == "WAIT_PASSWORD":
                matched, _ = match_prompt(data, pass_prompts)
                if matched:
                    recorder.event("SEND", "PASSWORD")
                    tn.write(password.encode() + b"\n")
                    state = "WAIT_PROMPT"

            elif state == "WAIT_PROMPT":
                if CLI_PROMPT.search(data):
                    break

        # ------------------------------
        # ENABLE MODE
        # ------------------------------
        if raw.strip().endswith(">"):
            recorder.event("SEND", "enable")
            tn.write(b"enable\n")
            time.sleep(0.5)

            if ENABLE_PASSWORD:
                recorder.event("SEND", "ENABLE_PASSWORD")
                tn.write(ENABLE_PASSWORD.encode() + b"\n")
                wait_for_prompt()

        # ------------------------------
        # Disable Paging
        # ------------------------------
        recorder.raw("\n")
        recorder.event("SEND", "terminal length 0")
        tn.write(b"terminal length 0\n")
        time.sleep(0.5)

        out = read()
        if "% Unrecognized" in out or "% Invalid" in out:
            recorder.event("SEND", "terminal datadump")
            tn.write(b"terminal datadump\n")
            wait_for_prompt()

        # ------------------------------
        # Execute Show Command
        # ------------------------------
        recorder.event("CMD_START", SHOW_CMD)
        recorder.event("SEND", SHOW_CMD)
        tn.write(SHOW_CMD.encode() + b"\n")

        while True:
            data = read()

            if data and CLI_PROMPT.search(data):
                recorder.event("CMD_END", SHOW_CMD)
                break

            if time.time() - last_rx > IDLE_TIMEOUT:
                recorder.event("CMD_END", SHOW_CMD)
                break

            time.sleep(0.2)

        status = "SUCCESS"
        tn.close()

    except Exception as e:
        status = f"FAILED: {e}"
        recorder.event("ERROR", str(e))

    finally:
        recorder.close(status)

    if status != "SUCCESS":
        raise RuntimeError(status)

    return raw
