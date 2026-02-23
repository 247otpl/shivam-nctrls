# backend/modules/inventory/service.py

from pathlib import Path
from datetime import datetime
import json
import paramiko

from .vendor_detection import resolve_vendor
from .adapters import get_adapter
from .mini_executor import MiniExecutor
from backend.api.routes.provisioning import get_registry_path, load_registry
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

    # Respect manual override
    if field.get("source") == "manual":
        return field

    field["value"] = new_value
    field["source"] = "auto"
    field["last_updated"] = datetime.now().isoformat()

    return field


# -------------------------------------------------
# MAIN COLLECTION FUNCTION
# -------------------------------------------------

def collect_device_inventory(base_dir, org_id, site_id, device):

    inventory_path = get_inventory_path(base_dir, org_id, site_id)
    inventory_data = load_inventory(inventory_path)

    existing = next(
        (d for d in inventory_data if d["device_id"] == device["device_id"]),
        None
    )

    # -------------------------------------------------
    # CREATE BASE RECORD IF NOT EXIST
    # -------------------------------------------------

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
    # RESOLVE VENDOR (Priority-Based)
    # -------------------------------------------------

    vendor = resolve_vendor(device, existing, base_dir)

    # Ensure vendor field exists
    if "vendor" not in existing["inventory"]:
        existing["inventory"]["vendor"] = {
            "value": "",
            "source": "auto",
            "last_updated": ""
        }

    # Update vendor field safely
    existing["inventory"]["vendor"] = update_field(
        existing["inventory"]["vendor"],
        vendor
    )

    # -------------------------------------------------
    # LOAD ADAPTER
    # -------------------------------------------------

    adapter = get_adapter(vendor)

    # -------------------------------------------------
    # SSH CONNECTION
    # -------------------------------------------------

    raw_output = ""
    status = "SUCCESS"

    try:
        executor = MiniExecutor()
        commands = adapter.collect_commands()
        raw_output = executor.run_commands(device, commands)

        collected = adapter.parse(raw_output)

    except Exception:
        collected = {}
        status = "FAILED"

    # Detect changes before update
    changes = detect_inventory_changes(existing["inventory"], collected)

    # Store change log
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

    # -------------------------------------------------
    # FINAL STATUS UPDATE
    # -------------------------------------------------

    existing["last_inventory_collection_status"] = status
    existing["last_inventory_collection_time"] = datetime.now().isoformat()

    save_inventory(inventory_path, inventory_data)

    return existing



# -------------------------------------------------
# BULK COLLECTION FUNCTION SITE-WIDE
# -------------------------------------------------
from concurrent.futures import ThreadPoolExecutor, as_completed


def collect_site_inventory(base_dir, org_id, site_id):

    registry_path = get_registry_path(base_dir, org_id, site_id)

    if not registry_path.exists():
        return {
            "status": "FAILED",
            "reason": "Device registry not found"
        }

    devices = load_registry(registry_path)

    results = []
    success = 0
    failed = 0

    with ThreadPoolExecutor(max_workers=10) as executor:

        future_to_device = {
            executor.submit(
                collect_device_inventory,
                base_dir,
                org_id,
                site_id,
                device
            ): device for device in devices
        }

        for future in as_completed(future_to_device):

            device = future_to_device[future]

            try:
                result = future.result()

                status = result["last_inventory_collection_status"]

                if status == "SUCCESS":
                    success += 1
                else:
                    failed += 1

                results.append({
                    "device_id": device["device_id"],
                    "status": status
                })

            except Exception:
                failed += 1
                results.append({
                    "device_id": device["device_id"],
                    "status": "FAILED"
                })

    return {
        "org_id": org_id,
        "site_id": site_id,
        "total_devices": len(devices),
        "successful": success,
        "failed": failed,
        "results": results
    }
