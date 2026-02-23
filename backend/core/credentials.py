#backend/core/credentials.py

from pathlib import Path
from backend.core.security import SecurityManager


# -------------------------------------------------
# SAVE ENCRYPTED CREDENTIALS
# -------------------------------------------------
def save_credentials(
    cred_dir: Path,
    username: str,
    password: str,
    base_dir: Path,
):

    cred_dir.mkdir(parents=True, exist_ok=True)

    security = SecurityManager(base_dir)

    encrypted = security.encrypt(f"{username}:{password}")

    with open(cred_dir / "creds.enc", "wb") as f:
        f.write(encrypted)


# -------------------------------------------------
# LOAD AND DECRYPT CREDENTIALS
# -------------------------------------------------
def load_credentials(
    cred_dir: Path,
    base_dir: Path,
):

    enc_file = cred_dir / "creds.enc"

    if not enc_file.exists():
        raise FileNotFoundError(
            "Encrypted credentials not configured for this module."
        )

    security = SecurityManager(base_dir)

    encrypted = enc_file.read_bytes()

    decrypted = security.decrypt(encrypted)

    if ":" not in decrypted:
        raise ValueError("Corrupted credential format.")

    username, password = decrypted.split(":", 1)

    return username, password
