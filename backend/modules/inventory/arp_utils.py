# backend/modules/inventory/arp_utils.py

import subprocess
import re


def normalize_mac(mac):
    mac = mac.lower().replace("-", ":")
    return mac


def get_mac_from_arp(ip):
    """
    Windows ARP lookup.
    Returns MAC address or None.
    """

    try:
        subprocess.run(["ping", "-n", "2", ip], stdout=subprocess.DEVNULL)

        output = subprocess.check_output(["arp", "-a", ip]).decode()

        match = re.search(r"([0-9a-fA-F\-]{17})", output)

        if match:
            return normalize_mac(match.group(1))

    except Exception:
        return None

    return None
