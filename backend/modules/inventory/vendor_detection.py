# backend/modules/inventory/vendor_detection.py

import subprocess
import re
import json
from pathlib import Path
from .arp_utils import get_mac_from_arp


# -------------------------------------------------
# PING DEVICE (Windows)
# -------------------------------------------------
def ping_device(ip: str):

    subprocess.run(
        ["ping", ip, "-n", "2"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


# -------------------------------------------------
# GET MAC FROM ARP (Windows)
# -------------------------------------------------
def get_mac_from_arp(ip: str):

    try:
        result = subprocess.run(
            ["arp", "-a", ip],
            capture_output=True,
            text=True
        )

        output = result.stdout

        # Match MAC pattern like f0-09-0d-d8-7c-6e
        match = re.search(
            r"([0-9a-fA-F]{2}-){5}[0-9a-fA-F]{2}",
            output
        )

        if match:
            return match.group(0)

        return None

    except Exception:
        return None


# -------------------------------------------------
# LOAD OUI DATABASE
# -------------------------------------------------
def load_oui_db(base_dir: Path):

    path = (
        base_dir
        / "backend"
        / "modules"
        / "inventory"
        / "oui_db.json"
    )

    if not path.exists():
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# -------------------------------------------------
# DETECT VENDOR FROM MAC
# -------------------------------------------------
def detect_vendor_from_mac(mac: str, oui_db: dict):

    normalized = mac.upper().replace("-", "").replace(":", "")
    prefix = normalized[:6]

    return oui_db.get(prefix)


# -------------------------------------------------
# RESOLVE VENDOR (FINAL PRIORITY LOGIC)
# -------------------------------------------------
def resolve_vendor(device, existing, base_dir):

    # 1️⃣ Manual override
    if existing:
        inv = existing.get("inventory", {})
        vendor_field = inv.get("vendor")
        if vendor_field and vendor_field.get("source") == "manual":
            return vendor_field.get("value")

    # 2️⃣ Device registry
    if device.get("vendor"):
        return device["vendor"]

    # 3️⃣ ARP lookup
    mac = get_mac_from_arp(device["mgmt_ip"])

    if not mac:
        return "unknown"

    oui = mac.replace(":", "")[:6].upper()

    oui_path = base_dir / "backend" / "modules" / "inventory" / "oui_db.json"

    if not oui_path.exists():
        return "unknown"

    oui_db = json.loads(oui_path.read_text())

    return oui_db.get(oui, "unknown")
