# backend/modules/inventory/service.py

from pathlib import Path
from datetime import datetime, timezone
import json

from backend.core.execution_planner import ExecutionPlanner
from backend.core.credentials import load_credentials

from .vendor_detection import resolve_vendor
from .adapters import get_adapter
from .mini_executor import MiniExecutor
from .change_detector import detect_inventory_changes


# -------------------------------------------------
# PATH HELPERS
# -------------------------------------------------

def get_inventory_path(base_dir, org_id, site_id):

    path = (
        base_dir
        / "data"
        / "orgs"
        / org_id
        / "sites"
        / site_id
        / "inventory"
        / "inventory.json"
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def get_debug_path(base_dir, org_id, site_id):

    path = (
        base_dir
        / "data"
        / "orgs"
        / org_id
        / "sites"
        / site_id
        / "inventory"
        / "debug_raw"
    )

    path.mkdir(parents=True, exist_ok=True)
    return path


def load_inventory(path):
    if not path.exists():
        return []
    return json.loads(path.read_text())


def save_inventory(path, data):
    path.write_text(json.dumps(data, indent=4))


# -------------------------------------------------
# FIELD UPDATE LOGIC
# -------------------------------------------------

def update_field(field, new_value):

    if field.get("source") == "manual":
        return field

    field["value"] = new_value
    field["source"] = "auto"
    field["last_updated"] = (
        datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )

    return field


# -------------------------------------------------
# SINGLE DEVICE COLLECTION
# -------------------------------------------------

def collect_device_inventory(base_dir, org_id, site_id, device):

    inventory_path = get_inventory_path(base_dir, org_id, site_id)
    debug_path = get_debug_path(base_dir, org_id, site_id)

    inventory_data = load_inventory(inventory_path)

    existing = next(
        (d for d in inventory_data if d["device_id"] == device["device_id"]),
        None
    )

    if not existing:
        existing = {
            "device_id": device["device_id"],
            "mgmt_ip": device["mgmt_ip"],
            "inventory": {},
            "commercial": {
                "customer_order_no": "",
                "vendor_dc_ref_no": "",
                "support_contract_no": "",
                "support_start_date": "",
                "support_end_date": ""
            },
            "last_inventory_collection_status": "NEVER",
            "last_inventory_collection_time": ""
        }

        inventory_data.append(existing)

    # -------------------------------------------------
    # LOAD CREDENTIALS
    # -------------------------------------------------

    site_dir = (
        base_dir
        / "data"
        / "orgs"
        / org_id
        / "sites"
        / site_id
    )

    cred_dir = site_dir / "config_backup" / "credentials"
    username, password = load_credentials(cred_dir, base_dir)

    # -------------------------------------------------
    # VENDOR RESOLUTION
    # -------------------------------------------------

    vendor = resolve_vendor(device, existing, base_dir)

    if "vendor" not in existing["inventory"]:
        existing["inventory"]["vendor"] = {
            "value": "",
            "source": "auto",
            "last_updated": ""
        }

    existing["inventory"]["vendor"] = update_field(
        existing["inventory"]["vendor"],
        vendor
    )

    adapter = get_adapter(vendor)

    # -------------------------------------------------
    # COMMAND EXECUTION
    # -------------------------------------------------

    raw_output = ""
    status = "SUCCESS"

    try:
        executor = MiniExecutor(username=username, password=password)
        commands = adapter.collect_commands()
        
        print("DEVICE:", device["device_id"])
        print("VENDOR:", vendor)
        print("COMMANDS:", commands)

        raw_output = executor.run_commands(device, commands)

        # Save raw debug
        debug_file = debug_path / f"{device['device_id']}.txt"
        debug_file.write_text(raw_output)

        collected = adapter.parse(raw_output)

    except Exception as e:
        print("INVENTORY ERROR:", device["device_id"])
        print("ERROR TYPE:", type(e))
        print("ERROR:", str(e))
        collected = {}
        status = "FAILED"
    
    # -------------------------------------------------
    # CHANGE DETECTION
    # -------------------------------------------------

    changes = detect_inventory_changes(existing["inventory"], collected)

    if changes:
        if "change_log" not in existing:
            existing["change_log"] = []
        existing["change_log"].extend(changes)

    # -------------------------------------------------
    # UPDATE INVENTORY FIELDS
    # -------------------------------------------------

    for key in [
        "hostname",
        "vendor",
        "platform",
        "model",
        "serial_number",
        "os_version",
        "hardware_version"
    ]:

        if key not in existing["inventory"]:
            existing["inventory"][key] = {
                "value": "",
                "source": "auto",
                "last_updated": ""
            }

        if key in collected:
            existing["inventory"][key] = update_field(
                existing["inventory"][key],
                collected[key]
            )

    existing["last_inventory_collection_status"] = status
    existing["last_inventory_collection_time"] = (
        datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )

    save_inventory(inventory_path, inventory_data)

    return existing


# -------------------------------------------------
# SITE COLLECTION (NO THREADING)
# -------------------------------------------------

def collect_site_inventory(base_dir, org_id, site_id):

    planner = ExecutionPlanner(base_dir)

    devices = planner.get_devices(
        org_id=org_id,
        site_id=site_id,
        mode="site"
    )

    results = []
    success = 0
    failed = 0

    for device in devices:

        result = collect_device_inventory(
            base_dir,
            org_id,
            site_id,
            device
        )

        status = result["last_inventory_collection_status"]

        if status == "SUCCESS":
            success += 1
        else:
            failed += 1

        results.append({
            "device_id": device["device_id"],
            "status": status
        })

    return {
        "org_id": org_id,
        "site_id": site_id,
        "total_devices": len(devices),
        "successful": success,
        "failed": failed,
        "results": results
    }