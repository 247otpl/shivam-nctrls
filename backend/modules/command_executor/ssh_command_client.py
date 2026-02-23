# backend/modules/command_executor/ssh_command_client.py

import paramiko
import time


class SSHCommandSession:
    def __init__(self, shell, prompt="#", timeout=5):
        self.shell = shell
        self.prompt = prompt
        self.timeout = timeout

    def send(self, command):
        self.shell.send(command + "\n")
        output = ""
        end = time.time() + self.timeout

        while time.time() < end:
            if self.shell.recv_ready():
                chunk = self.shell.recv(65535).decode(errors="ignore")
                output += chunk
                if output.strip().endswith(self.prompt):
                    break
            time.sleep(0.1)

        return output.strip()


def run_ssh_command_mode(ip, port, username, password, enable_password=None):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(
        ip,
        port=port,
        username=username,
        password=password,
        look_for_keys=False,
        allow_agent=False,
        timeout=10,
    )

    shell = client.invoke_shell()
    time.sleep(1)

    raw = ""
    if shell.recv_ready():
        raw = shell.recv(65535).decode(errors="ignore")

    if raw.strip().endswith(">"):
        shell.send("enable\n")
        time.sleep(0.5)
        if enable_password:
            shell.send(enable_password + "\n")
            time.sleep(0.5)

    return SSHCommandSession(shell)
