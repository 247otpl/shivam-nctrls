# backenc/core/security.py

from cryptography.fernet import Fernet
from pathlib import Path


class SecurityManager:
    def __init__(self, base_dir: Path):
        self.data_dir = base_dir / "data"
        self.key_file = self.data_dir / "app.key"
        self._ensure_key()

    # -------------------------------------------------
    # MASTER KEY
    # -------------------------------------------------
    def _ensure_key(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)

        if not self.key_file.exists():
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(key)

    def _get_cipher(self):
        with open(self.key_file, "rb") as f:
            key = f.read()
        return Fernet(key)

    # -------------------------------------------------
    # ENCRYPT / DECRYPT
    # -------------------------------------------------
    def encrypt(self, plaintext: str) -> bytes:
        cipher = self._get_cipher()
        return cipher.encrypt(plaintext.encode())

    def decrypt(self, encrypted: bytes) -> str:
        cipher = self._get_cipher()
        return cipher.decrypt(encrypted).decode()
