# backend/api/routes/inventory.py

from fastapi import APIRouter, HTTPException
from pathlib import Path
import json

from backend.modules.inventory.service import collect_device_inventory
from backend.api.routes.provisioning import get_registry_path, load_registry
from backend.modules.inventory.service import collect_site_inventory
from backend.modules.inventory.contract_monitor import evaluate_site_contracts
from backend.modules.inventory.contract_monitor import evaluate_site_contracts
from backend.core.execution_planner import ExecutionPlanner


router = APIRouter()


@router.post("/collect")
def collect_inventory(org_id: str, site_id: str, device_id: str):

    BASE_DIR = Path(__file__).resolve().parents[3]

    planner = ExecutionPlanner(BASE_DIR)

    devices = planner.get_devices(
        org_id=org_id,
        site_id=site_id,
        mode="site"
    )
    
    device = next(
        (d for d in devices if d["device_id"] == device_id),
        None
    )

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    result = collect_device_inventory(
        BASE_DIR, org_id, site_id, device
    )

    return result


@router.get("/list")
def list_inventory(org_id: str, site_id: str):

    BASE_DIR = Path(__file__).resolve().parents[3]

    path = (
        BASE_DIR
        / "data"
        / "orgs"
        / org_id
        / "sites"
        / site_id
        / "inventory"
        / "inventory.json"
    )

    if not path.exists():
        return []

    return json.loads(path.read_text())


@router.post("/collect-all")
def collect_all_inventory(org_id: str, site_id: str):

    BASE_DIR = Path(__file__).resolve().parents[3]

    result = collect_site_inventory(BASE_DIR, org_id, site_id)

    return result


@router.get("/contracts")
def check_contracts(org_id: str, site_id: str, warning_days: int = 30):

    BASE_DIR = Path(__file__).resolve().parents[3]

    result = evaluate_site_contracts(
        BASE_DIR,
        org_id,
        site_id,
        warning_days
    )

    return result


@router.get("/contracts/summary")
def contract_summary(org_id: str, site_id: str):

    BASE_DIR = Path(__file__).resolve().parents[3]

    result = evaluate_site_contracts(BASE_DIR, org_id, site_id)

    summary = result.get("summary", {})

    return {
        "expired": summary.get("expired", 0),
        "expiring_soon": summary.get("expiring_soon", 0),
        "no_contract": summary.get("no_contract", 0),
        "active": summary.get("active", 0)
    }
