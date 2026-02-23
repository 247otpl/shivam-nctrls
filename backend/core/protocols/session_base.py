# backend/core/protocols/session_base.py

import time
from abc import ABC, abstractmethod


class SessionBase(ABC):

    # -------------------------------------------------
    # REQUIRED ENGINE METHODS
    # -------------------------------------------------

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def send(self, command: str):
        pass

    @abstractmethod
    def receive(self) -> str:
        pass

    @abstractmethod
    def close(self):
        pass

    # -------------------------------------------------
    # PROMPT DETECTION
    # -------------------------------------------------

    def _is_prompt_detected(self, text: str) -> bool:

        if not text:
            return False

        lines = text.strip().splitlines()
        if not lines:
            return False

        # Check last 3 lines (TP-Link sometimes appends logs)
        last_lines = lines[-3:]

        for line in reversed(last_lines):
            clean_line = line.strip()

            # Ignore paging artifacts
            if "--More--" in clean_line:
                continue

            # Ignore syslog-style lines
            if clean_line.startswith("#20"):
                continue

            # Typical CLI prompts
            if clean_line.endswith("#"):
                return True

            if clean_line.endswith(">"):
                return True

        return False
        
    # -------------------------------------------------
    # PAGING + PROMPT INTELLIGENCE
    # -------------------------------------------------

    def read_until_prompt(self, timeout=30):

        buffer = ""
        start_time = time.time()

        paging_patterns = [
            "--More--",
            "More:",
            "(q)uit",
            "Press any key",
            "<--- More --->"
        ]

        while True:

            chunk = self.receive()
            if chunk:
                buffer += chunk

                # Detect paging
                for pattern in paging_patterns:
                    if pattern in buffer:
                        self.send(" ")
                        buffer = buffer.replace(pattern, "")
                        break

            # Detect prompt
            if self._is_prompt_detected(buffer):
                break

            # Timeout protection
            if time.time() - start_time > timeout:
                break

            time.sleep(0.2)

        return buffer

    # -------------------------------------------------
    # ENABLE MODE SUPPORT
    # -------------------------------------------------

    def ensure_enable_mode(self, enable_password=None):

        self.send("")
        output = self.read_until_prompt()

        lines = output.strip().splitlines()
        if not lines:
            return

        prompt = lines[-1].strip()

        # Already enabled
        if prompt.endswith("#"):
            return

        # Need to enter enable
        if prompt.endswith(">"):

            self.send("enable")
            output = self.read_until_prompt()

            if "Password" in output and enable_password:
                self.send(enable_password)
                self.read_until_prompt()
