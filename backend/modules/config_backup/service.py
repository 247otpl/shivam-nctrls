# backend/modules/config_backup/service.py

from pathlib import Path
import time
from datetime import datetime

from backend.core.execution_planner import ExecutionPlanner
from backend.core.client_settings import load_client_settings
from backend.core.credentials import load_credentials
from backend.core.diff_engine import DiffEngine

from backend.core.logging.config_backup_logger import ConfigBackupLogger

from backend.core.protocols.ssh_engine import SSHEngine
from backend.core.protocols.telnet_engine import TelnetEngine

from backend.modules.config_backup.utils import (
    RawRecorder,
    clean_config,
    extract_hostname,
    today_date,
    now_timestamp,
)


# -------------------------------------------------
# AUTH LOGGER
# -------------------------------------------------
def write_auth_log(log_dir: Path, message: str):
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "auth.log"

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{now_timestamp()}] {message}\n")


# -------------------------------------------------
# MAIN BACKUP
# -------------------------------------------------
def run_config_backup(
    base_dir: Path,
    org_id: str,
    site_id: str = None,
    mode: str = "all",
    device_ids=None,
    mgmt_ips=None,
):

    if not site_id:
        raise ValueError("site_id is required for config backup")

    planner = ExecutionPlanner(base_dir)

    devices = planner.get_devices(
        org_id=org_id,
        site_id=site_id,
        mode=mode,
        device_ids=device_ids,
        mgmt_ips=mgmt_ips,
    )

    site_dir = (
        base_dir
        / "data"
        / "orgs"
        / org_id
        / "sites"
        / site_id
    )

    module_dir = site_dir / "config_backup"

    backup_root = module_dir / "backups"
    report_root = module_dir / "reports"
    debug_root = module_dir / "debug_raw"
    log_root = module_dir / "logs"
    cred_dir = module_dir / "credentials"

    today_folder = today_date()

    backup_dir = backup_root / today_folder
    report_dir = report_root / today_folder
    log_dir = log_root / today_folder

    backup_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------
    # STRUCTURED EXECUTION LOGGER
    # -------------------------------------------------
    logger = ConfigBackupLogger(
        base_dir=base_dir,
        org_id=org_id,
        site_id=site_id,
    )

    username, password = load_credentials(cred_dir, base_dir)

    results = []

    for device in devices:

        device_id = device["device_id"]
        ip = device["mgmt_ip"]
        protocol = device.get("protocol", "ssh")
        last_octet = ip.split(".")[-1]

        recorder = None
        raw_text = ""

        try:

            settings = load_client_settings(
                base_dir,
                org_id,
                site_id,
                "config_backup"
            )

            engine = None

            if protocol == "ssh":

                engine = SSHEngine(
                    host=ip,
                    username=username,
                    password=password,
                    port=settings.get("ssh_port", 22),
                    timeout=settings.get("timeout", 10),
                )

            elif protocol == "telnet":

                engine = TelnetEngine(
                    host=ip,
                    username=username,
                    password=password,
                    port=settings.get("telnet_port", 23),
                    timeout=settings.get("timeout", 10),
                )

            elif protocol == "both":

                try:
                    # Try SSH first
                    engine = SSHEngine(
                        host=ip,
                        username=username,
                        password=password,
                        port=settings.get("ssh_port", 22),
                        timeout=settings.get("timeout", 10),
                    )
                    engine.connect()
                    actual_protocol = "ssh"

                except Exception:

                    # Fallback to Telnet
                    engine = TelnetEngine(
                        host=ip,
                        username=username,
                        password=password,
                        port=settings.get("telnet_port", 23),
                        timeout=settings.get("timeout", 10),
                    )
                    engine.connect()
                    actual_protocol = "telnet"

                protocol = actual_protocol  # override for logging

            elif protocol == "none":

                raise Exception("No usable protocol configured for device")

            else:
                raise Exception(f"Unsupported protocol: {protocol}")

            recorder = RawRecorder(ip, protocol, debug_root)

            if protocol != "both":
                engine.connect()

            # Ensure enable mode BEFORE sending commands
            engine.ensure_enable_mode(
                enable_password=settings.get("enable_password")
            )

            write_auth_log(
                log_dir,
                f"{device_id} ({ip}) AUTH SUCCESS via {protocol}"
            )

            time.sleep(1)

            banner = engine.receive()
            raw_text += banner
            recorder.raw(banner)

            commands_file = module_dir / "commands.txt"
            commands = [
                line.strip()
                for line in commands_file.read_text().splitlines()
                if line.strip()
            ]

            for cmd in commands:
                engine.send(cmd)
                buffer = engine.read_until_prompt(timeout=40)
                raw_text += buffer
                recorder.raw(buffer)

            engine.close()
            recorder.close("SUCCESS")

            # -------------------------------------------------
            # CLEAN CONFIG
            # -------------------------------------------------
            cleaned = clean_config(raw_text)
            hostname = extract_hostname(raw_text, fallback=device_id)

            # -------------------------------------------------
            # VERSIONING
            # -------------------------------------------------
            existing_files = list(
                backup_dir.glob(f"{hostname}-{last_octet}_v*.txt")
            )

            versions = []

            for f in existing_files:
                name = f.stem
                if "_v" in name:
                    try:
                        v = int(name.split("_v")[-1])
                        versions.append(v)
                    except:
                        pass

            next_version = max(versions) + 1 if versions else 1

            filename = f"{hostname}-{last_octet}_v{next_version}.txt"
            current_file = backup_dir / filename
            current_file.write_text(cleaned)

            # -------------------------------------------------
            # DIFF
            # -------------------------------------------------
            previous_versions = sorted(
                backup_dir.glob(f"{hostname}-{last_octet}_v*.txt"),
                key=lambda x: int(x.stem.split("_v")[-1]),
                reverse=True
            )

            previous_file = None
            for f in previous_versions:
                if f != current_file:
                    previous_file = f
                    break

            if previous_file:
                diff_txt = report_dir / f"{hostname}_{last_octet}_diff.txt"
                diff_html = report_dir / f"{hostname}_{last_octet}_diff.html"

                DiffEngine.generate_diff(
                    previous_file,
                    current_file,
                    diff_txt,
                    diff_html
                )

            # -------------------------------------------------
            # SUCCESS LOGGING
            # -------------------------------------------------
            logger.add_device_result(device_id, "SUCCESS")

            results.append(
                {
                    "device_id": device_id,
                    "hostname": hostname,
                    "status": "SUCCESS"
                }
            )

        except Exception as e:

            write_auth_log(
                log_dir,
                f"{device_id} ({ip}) AUTH FAILED via {protocol} - {str(e)}"
            )

            if recorder:
                recorder.close("FAILED")

            logger.add_device_result(device_id, "FAILED", str(e))

            results.append(
                {
                    "device_id": device_id,
                    "status": "FAILED",
                    "error": str(e)
                }
            )

    # -------------------------------------------------
    # FINALIZE EXECUTION LOG
    # -------------------------------------------------
    logger.finalize()

    return {
        "org_id": org_id,
        "site_id": site_id,
        "mode": mode,
        "total_devices": len(devices),
        "results": results
    }
