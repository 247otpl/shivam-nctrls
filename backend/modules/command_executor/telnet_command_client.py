# backend/modules/command_executor/telnet_command_client.py

import telnetlib
import time


class TelnetCommandSession:
    def __init__(self, tn, prompt=b"#", timeout=5):
        self.tn = tn
        self.prompt = prompt
        self.timeout = timeout

    def send(self, command):
        self.tn.write(command.encode() + b"\n")
        output = b""
        end = time.time() + self.timeout

        while time.time() < end:
            try:
                chunk = self.tn.read_very_eager()
                if chunk:
                    output += chunk
                    if output.rstrip().endswith(self.prompt):
                        break
            except Exception:
                break
            time.sleep(0.1)

        return output.decode(errors="ignore").strip()


def run_telnet_command_mode(ip, port, username, password, enable_password=None):
    tn = telnetlib.Telnet(ip, port, timeout=10)

    tn.read_until(b":")
    tn.write(username.encode() + b"\n")
    tn.read_until(b":")
    tn.write(password.encode() + b"\n")
    time.sleep(1)

    raw = b""
    try:
        raw = tn.read_very_eager()
    except Exception:
        pass

    if raw.strip().endswith(b">"):
        tn.write(b"enable\n")
        time.sleep(0.5)
        if enable_password:
            tn.write(enable_password.encode() + b"\n")
            time.sleep(0.5)

    return TelnetCommandSession(tn)
