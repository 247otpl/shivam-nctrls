# backend/modules/command_executor/service.py

from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Semaphore
from pathlib import Path
import queue

from backend.core.execution_planner import ExecutionPlanner
from backend.core.client_settings import load_client_settings
from backend.core.credentials import load_credentials

#from backend.core.execution_logger import ExecutionLogger
from backend.core.logging.command_executor_logger import CommandExecutorLogger

from backend.core.job_manager import job_manager

from backend.core.protocols.ssh_engine import SSHEngine
from backend.core.protocols.telnet_engine import TelnetEngine

from backend.modules.config_backup.utils import (
    RawRecorder,
    now_timestamp,
)


# -------------------------------------------------
# SIMPLE EXECUTION LOG FILE
# -------------------------------------------------
def write_exec_log(log_dir: Path, message: str):
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "execution.log"

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{now_timestamp()}] {message}\n")


# -------------------------------------------------
# DEVICE EXECUTION WORKER
# -------------------------------------------------
def execute_device(
    device,
    run_id,
    base_dir,
    org_id,
    site_id,
    module_dir,
    log_root,
    debug_root,
    output_root,
    username,
    password,
    commands,
    logger,
    ssh_semaphore,
    telnet_semaphore,
    event_queue=None,
    dry_run=False,
):

    device_id = device["device_id"]
    ip = device["mgmt_ip"]

    # 🔴 CANCEL CHECK (BEFORE START)
    if job_manager.is_cancelled(run_id):
        return {"device_id": device_id, "status": "CANCELLED"}

    protocol = device.get("protocol", "ssh")

    settings = load_client_settings(
        base_dir,
        org_id,
        site_id,
        "command_executor"
    )

    device_timeout = device.get(
        "timeout",
        settings.get("timeout", 10)
    )

    if dry_run:
        job_manager.mark_completed(run_id)

        return {"device_id": device_id, "status": "DRY_RUN"}

    raw_output = ""
    recorder = None

    try:
        engine = None

        # -----------------------------
        # PROTOCOL HANDLING
        # -----------------------------
        if protocol == "ssh":
            with ssh_semaphore:
                engine = SSHEngine(
                    host=ip,
                    username=username,
                    password=password,
                    port=settings.get("ssh_port", 22),
                    timeout=device_timeout,
                )
                engine.connect()

        elif protocol == "telnet":
            with telnet_semaphore:
                engine = TelnetEngine(
                    host=ip,
                    username=username,
                    password=password,
                    port=settings.get("telnet_port", 23),
                    timeout=device_timeout,
                )
                engine.connect()

        elif protocol == "both":
            try:
                with ssh_semaphore:
                    engine = SSHEngine(
                        host=ip,
                        username=username,
                        password=password,
                        port=settings.get("ssh_port", 22),
                        timeout=device_timeout,
                    )
                    engine.connect()
                    protocol = "ssh"
            except Exception:
                with telnet_semaphore:
                    engine = TelnetEngine(
                        host=ip,
                        username=username,
                        password=password,
                        port=settings.get("telnet_port", 23),
                        timeout=device_timeout,
                    )
                    engine.connect()
                    protocol = "telnet"
        else:
            raise Exception("Invalid protocol configured")

        write_exec_log(
            log_root,
            f"{device_id} ({ip}) CONNECTED via {protocol}"
        )

        recorder = RawRecorder(ip, protocol, debug_root)

        # 🔴 CANCEL CHECK (AFTER CONNECT)
        if job_manager.is_cancelled(run_id):
            engine.close()
            return {"device_id": device_id, "status": "CANCELLED"}

        # -----------------------------
        # COMMAND EXECUTION
        # -----------------------------
        for cmd in commands:

            # 🔴 CANCEL CHECK (BEFORE EACH COMMAND)
            if job_manager.is_cancelled(run_id):
                engine.close()
                return {"device_id": device_id, "status": "CANCELLED"}

            engine.send(cmd)
            buffer = engine.read_until_prompt()
            raw_output += buffer
            recorder.raw(buffer)

        engine.close()
        recorder.close("SUCCESS")

        device_output_file = output_root / f"{device_id}.txt"
        device_output_file.write_text(raw_output, encoding="utf-8")

        logger.add_device_result(
            device_id,
            "SUCCESS",
            extra={
                "protocol_used": protocol,
                "output_file": str(device_output_file)
            }
        )

        # 🔵 MARK PROGRESS
        job_manager.mark_completed(run_id)

        if event_queue:
            event_queue.put({
                "type": "progress",
                "data": job_manager.get_status(run_id)
            })

        return {"device_id": device_id, "status": "SUCCESS"}

    except Exception as e:

        if recorder:
            recorder.close("FAILED")

        write_exec_log(
            log_root,
            f"{device_id} ({ip}) FAILED - {str(e)}"
        )

        logger.add_device_result(device_id, "FAILED", str(e))

        job_manager.mark_completed(run_id)

        if event_queue:
            event_queue.put({
                "type": "progress",
                "data": job_manager.get_status(run_id)
            })

        return {
            "device_id": device_id,
            "status": "FAILED",
            "error": str(e)
        }


# -------------------------------------------------
# MAIN EXECUTION FUNCTION
# -------------------------------------------------
def run_command_executor(
    base_dir: Path,
    org_id: str,
    site_id: str,
    mode: str = "all",
    device_ids=None,
    mgmt_ips=None,
    dry_run: bool = False,
    event_queue: queue.Queue = None,
):

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

    module_dir = site_dir / "command_executor"
    log_root = module_dir / "logs"
    debug_root = module_dir / "debug_raw"
    cred_dir = module_dir / "credentials"

    settings = load_client_settings(
        base_dir,
        org_id,
        site_id,
        "command_executor"
    )

    max_workers = settings.get("max_workers", 5)
    max_ssh = settings.get("max_ssh_workers", 5)
    max_telnet = settings.get("max_telnet_workers", 3)

    ssh_semaphore = Semaphore(max_ssh)
    telnet_semaphore = Semaphore(max_telnet)

    logger = CommandExecutorLogger(
        base_dir=base_dir,
        org_id=org_id,
        site_id=site_id,
    )

    run_id = logger.run_id

    # 🔵 REGISTER JOB
    job_manager.create_job(run_id, len(devices))

    output_root = module_dir / "outputs" / run_id
    output_root.mkdir(parents=True, exist_ok=True)

    username, password = load_credentials(cred_dir, base_dir)

    commands_file = module_dir / "commands.txt"
    if not commands_file.exists():
        raise Exception("commands.txt not found")

    commands = [
        line.strip()
        for line in commands_file.read_text().splitlines()
        if line.strip()
    ]

    results = []

    # -------------------------------------------------
    # PARALLEL EXECUTION
    # -------------------------------------------------
    with ThreadPoolExecutor(max_workers=max_workers) as executor:

        futures = [
            executor.submit(
                execute_device,
                device,
                run_id,
                base_dir,
                org_id,
                site_id,
                module_dir,
                log_root,
                debug_root,
                output_root,
                username,
                password,
                commands,
                logger,
                ssh_semaphore,
                telnet_semaphore,
                event_queue,
                dry_run,
            )
            for device in devices
        ]

        for future in as_completed(futures):
            results.append(future.result())

    # 🔵 FINALIZE JOB
    job_manager.finalize_job(run_id)

    if event_queue:
        event_queue.put({
            "type": "complete",
            "data": job_manager.get_status(run_id)
        })

    return {
        "run_id": run_id,
        "total_devices": len(devices),
        "results": results
    }
