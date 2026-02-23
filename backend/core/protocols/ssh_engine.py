# backend/core/protocols/ssh_engine.py

import paramiko
import time

from backend.core.protocols.session_base import SessionBase


class SSHEngine(SessionBase):

    def __init__(self, host, username, password, port, timeout):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout
        self.client = None
        self.shell = None

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(
            paramiko.AutoAddPolicy()
        )

        self.client.connect(
            hostname=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            timeout=self.timeout,
            look_for_keys=False,
            allow_agent=False,
        )

        self.shell = self.client.invoke_shell()
        time.sleep(1)

        self.read_until_prompt()

    def send(self, command: str):
        self.shell.send(command + "\n")

    def receive(self):
        output = ""
        time.sleep(0.5)

        while self.shell.recv_ready():
            output += self.shell.recv(65535).decode(errors="ignore")

        return output

    def close(self):
        if self.client:
            self.client.close()
