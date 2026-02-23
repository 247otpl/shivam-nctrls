# backend/modules/inventory/contract_monitor.py


from datetime import datetime
from pathlib import Path
import json


DEFAULT_EXPIRY_WARNING_DAYS = 30


def evaluate_contract(device_record, warning_days=DEFAULT_EXPIRY_WARNING_DAYS):

    commercial = device_record.get("commercial", {})
    end_date_str = commercial.get("support_end_date")

    result = {
        "device_id": device_record.get("device_id"),
        "status": "UNKNOWN",
        "days_remaining": None,
        "severity": "INFO"
    }

    if not end_date_str:
        result["status"] = "NO_CONTRACT"
        result["severity"] = "WARNING"
        return result

    try:
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError:
        result["status"] = "INVALID_DATE_FORMAT"
        result["severity"] = "WARNING"
        return result

    today = datetime.now()
    delta = (end_date - today).days

    result["days_remaining"] = delta

    if delta < 0:
        result["status"] = "EXPIRED"
        result["severity"] = "CRITICAL"
    elif delta <= warning_days:
        result["status"] = "EXPIRING_SOON"
        result["severity"] = "WARNING"
    else:
        result["status"] = "ACTIVE"
        result["severity"] = "OK"

    return result


def evaluate_site_contracts(base_dir, org_id, site_id, warning_days=DEFAULT_EXPIRY_WARNING_DAYS):

    inventory_path = (
        base_dir
        / "data"
        / "orgs"
        / org_id
        / "sites"
        / site_id
        / "inventory"
        / "inventory.json"
    )

    if not inventory_path.exists():
        return {
            "status": "FAILED",
            "reason": "Inventory not found"
        }

    inventory_data = json.loads(inventory_path.read_text())

    results = []
    summary = {
        "total": 0,
        "expired": 0,
        "expiring_soon": 0,
        "no_contract": 0,
        "active": 0
    }

    for device in inventory_data:

        evaluation = evaluate_contract(device, warning_days)

        results.append(evaluation)
        summary["total"] += 1

        if evaluation["status"] == "EXPIRED":
            summary["expired"] += 1
        elif evaluation["status"] == "EXPIRING_SOON":
            summary["expiring_soon"] += 1
        elif evaluation["status"] == "NO_CONTRACT":
            summary["no_contract"] += 1
        elif evaluation["status"] == "ACTIVE":
            summary["active"] += 1

    return {
        "org_id": org_id,
        "site_id": site_id,
        "summary": summary,
        "devices": results
    }
