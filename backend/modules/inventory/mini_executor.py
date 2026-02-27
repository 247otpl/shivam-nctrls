# backend/modules/inventory/mini_executor.py

from backend.core.protocols.ssh_engine import SSHEngine


class MiniExecutor:

    def __init__(self, username, password, timeout=10):
        self.username = username
        self.password = password
        self.timeout = timeout

    def run_commands(self, device, commands):

        engine = SSHEngine(
            host=device["mgmt_ip"],
            username=self.username,
            password=self.password,
            port=22,
            timeout=self.timeout
        )

        engine.connect()
        engine.ensure_enable_mode()

        raw_output = ""

        for cmd in commands:
            engine.send(cmd)
            raw_output += engine.read_until_prompt(timeout=30)

        engine.close()

        return raw_output