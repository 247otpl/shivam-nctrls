# backend/modules/inventory/mini_executor.py

import paramiko


class MiniExecutor:

    def __init__(self, timeout=10):
        self.timeout = timeout

    def run_commands(self, device, commands):
        """
        Execute list of commands over SSH.
        Returns raw combined output string.
        Raises exception if connection fails.
        """

        raw_output = ""

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(
            hostname=device["mgmt_ip"],
            username=device.get("username"),
            password=device.get("password"),
            timeout=self.timeout
        )

        for cmd in commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            raw_output += stdout.read().decode(errors="ignore")

        ssh.close()

        return raw_output
