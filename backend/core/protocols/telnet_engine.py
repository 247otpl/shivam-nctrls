# backend/core/protocols/telnet_engine.py

import telnetlib
import time

from backend.core.protocols.session_base import SessionBase


class TelnetEngine(SessionBase):

    def __init__(self, host, username, password, port, timeout):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout
        self.connection = None

    def connect(self):
        self.connection = telnetlib.Telnet(
            self.host,
            self.port,
            self.timeout
        )

        time.sleep(1)

        # Basic login handling
        self.connection.read_until(b"Username:", timeout=5)
        self.connection.write(self.username.encode() + b"\n")

        self.connection.read_until(b"Password:", timeout=5)
        self.connection.write(self.password.encode() + b"\n")

        time.sleep(1)

        self.read_until_prompt()

    def send(self, command: str):
        self.connection.write(command.encode() + b"\n")

    def receive(self):
        time.sleep(0.5)
        try:
            return self.connection.read_very_eager().decode(errors="ignore")
        except:
            return ""

    def close(self):
        if self.connection:
            self.connection.close()
