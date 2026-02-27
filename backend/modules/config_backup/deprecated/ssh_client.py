# backend/modules/config_backup/ssh_client.py

import paramiko
import time
import re

from backend.modules.config_backup.settings import SHOW_CMD, ENABLE_PASSWORD
from backend.modules.config_backup.utils import RawRecorder

PROMPT_RE = re.compile(r"[>#]\s*$")


def run_ssh(ip, port, username, password, debug_base_path):
    recorder = RawRecorder(ip, "SSH", debug_base_path)
    raw = ""

    try:
        recorder.event("CONNECT", "SSH session starting")

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            ip,
            port=port,
            username=username,
            password=password,
            timeout=8,
            banner_timeout=5,
            auth_timeout=5,
            look_for_keys=False,
            allow_agent=False,
        )

        transport = client.get_transport()
        if transport:
            transport.set_keepalive(0)

        recorder.event("AUTH", "Authentication successful")

        chan = client.invoke_shell()
        chan.settimeout(3)

        time.sleep(0.5)  # reduced from 1 second

        def read():
            nonlocal raw
            data = ""
            while chan.recv_ready():
                chunk = chan.recv(65535).decode(errors="ignore")
                recorder.raw(chunk)
                data += chunk
            if data:
                raw += data
            return data

        def send(cmd):
            recorder.event("SEND", cmd)
            chan.send(cmd + "\n")
            time.sleep(0.3)  # reduced delay
            return read()

        # Initial banner
        read()

        # Enable mode if needed
        if PROMPT_RE.search(raw) and raw.strip().endswith(">"):
            send("enable")
            if ENABLE_PASSWORD:
                send(ENABLE_PASSWORD)

        # Disable pagination
        out = send("terminal length 0")
        if "%" in out:
            send("terminal datadump")

        recorder.event("CMD_START", SHOW_CMD)
        send(SHOW_CMD)

        # Intelligent read loop (max 10 seconds)
        end_time = time.time() + 10

        while time.time() < end_time:
            data = read()

            if data and PROMPT_RE.search(data):
                recorder.event("CMD_END", SHOW_CMD)
                break

            time.sleep(0.2)

        chan.close()
        client.get_transport().close()
        client.close()
        recorder.close("SUCCESS")
        return raw

    except Exception as e:
        recorder.event("ERROR", str(e))
        recorder.close("FAILED")
        raise
