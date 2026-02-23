# backend/modules/discovery/service.py

from pathlib import Path
import json
import ipaddress
import socket
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

from backend.core.logging.discovery_logger import DiscoveryLogger


# -------------------------------------------------
# ICMP CHECK
# -------------------------------------------------
def icmp_check(ip: str, timeout=1) -> bool:
    try:
        result = subprocess.run(
            ["ping", "-n", "1", "-w", str(timeout * 1000), ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except Exception:
        return False


# -------------------------------------------------
# TCP PORT CHECK
# -------------------------------------------------
def port_check(ip: str, port: int, timeout=1) -> bool:
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except Exception:
        return False


# -------------------------------------------------
# MAIN DISCOVERY FUNCTION
# -------------------------------------------------
def run_discovery_scan(
    base_dir: Path,
    org_id: str,
    site_id: str,
    subnet: str = None,
    start_ip: str = None,
    end_ip: str = None,
):

    if not subnet and not (start_ip and end_ip):
        raise ValueError("Provide either subnet or start_ip + end_ip")

    # -------------------------------------------------
    # INITIALIZE LOGGER
    # -------------------------------------------------
    logger = DiscoveryLogger(
        base_dir=base_dir,
        org_id=org_id,
        site_id=site_id,
    )

    run_id = logger.run_id

    # -------------------------------------------------
    # BUILD IP LIST
    # -------------------------------------------------
    if subnet:
        network = ipaddress.ip_network(subnet, strict=False)
        ip_list = [str(ip) for ip in network.hosts()]
    else:
        start = int(ipaddress.ip_address(start_ip))
        end = int(ipaddress.ip_address(end_ip))
        ip_list = [
            str(ipaddress.ip_address(ip))
            for ip in range(start, end + 1)
        ]

    # -------------------------------------------------
    # PREPARE SCAN FOLDER
    # -------------------------------------------------
    scan_dir = (
        base_dir
        / "data"
        / "orgs"
        / org_id
        / "sites"
        / site_id
        / "discovery"
        / "scans"
        / run_id
    )

    scan_dir.mkdir(parents=True, exist_ok=True)

    results = []

    # -------------------------------------------------
    # THREAD POOL SCAN
    # -------------------------------------------------
    def scan_ip(ip):

        icmp = icmp_check(ip)
        ssh = port_check(ip, 22)
        telnet = port_check(ip, 23)

        status = "DOWN"
        if icmp or ssh or telnet:
            status = "UP"

        logger.add_device_result(
            device_id=ip,
            status=status,
            extra={
                "icmp": icmp,
                "ssh_open": ssh,
                "telnet_open": telnet
            }
        )

        return {
            "ip": ip,
            "icmp": icmp,
            "ssh_open": ssh,
            "telnet_open": telnet
        }

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(scan_ip, ip) for ip in ip_list]
        for future in as_completed(futures):
            results.append(future.result())

    # -------------------------------------------------
    # SAVE RESULTS
    # -------------------------------------------------
    with open(scan_dir / "scan_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    # -------------------------------------------------
    # FINALIZE LOGGER (writes log + applies retention)
    # -------------------------------------------------
    logger.finalize()

    return {
        "org_id": org_id,
        "site_id": site_id,
        "scan_id": run_id,
        "status": "COMPLETED",
        "total_ips": len(ip_list)
    }
