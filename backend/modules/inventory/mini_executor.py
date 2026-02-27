# backend/modules/inventory/mini_executor.py

from backend.core.protocols.ssh_engine import SSHEngine
from backend.core.protocols.telnet_engine import TelnetEngine


class MiniExecutor:

    def __init__(self, username, password, timeout=30):
        self.username = username
        self.password = password
        self.timeout = timeout

    def _get_engine(self, device):

        host = device.get("mgmt_ip")

        if not host:
            raise ValueError(f"No mgmt_ip found for device {device.get('device_id')}")

        protocol = device.get("protocol", "ssh").lower()

        # Inventory allows "both"
        # Prefer SSH first, fallback to Telnet
        if protocol == "telnet":
            return TelnetEngine(
                host,
                23,
                self.username,
                self.password,
                self.timeout
            )

        # For "ssh" or "both" default to SSH
        return SSHEngine(
            host,
            22,
            self.username,
            self.password,
            self.timeout
        )

    def run_commands(self, device, commands):

        engine = self._get_engine(device)

        engine.connect()
        engine.open_shell()
        engine.initialize_session()

        raw_output = ""

        for cmd in commands:
            engine.send(cmd)
            output = engine.read_until_prompt(timeout=self.timeout)
            raw_output += output

        engine.close()

        return raw_output