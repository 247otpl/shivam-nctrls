# backend/api/routes/discovery.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
import json
import uuid
from datetime import datetime, timezone
import uuid

from backend.modules.discovery.service import run_discovery_scan

router = APIRouter()


# -------------------------------------------------
# MODEL
# -------------------------------------------------

class DiscoveryRequest(BaseModel):
    org_id: str
    site_id: str
    subnet: str = None
    start_ip: str = None
    end_ip: str = None


# -------------------------------------------------
# INTERNAL
# -------------------------------------------------

def get_discovery_root(base_dir: Path, org_id: str, site_id: str):

    site_path = (
        base_dir
        / "data"
        / "orgs"
        / org_id
        / "sites"
        / site_id
    )

    if not site_path.exists():
        raise HTTPException(status_code=404, detail="Org/Site not found")

    return site_path / "discovery" / "scans"

# -------------------------------------------------
# 1️⃣ START SCAN
# -------------------------------------------------

@router.post("/scan")
def scan_network(request: DiscoveryRequest):

    try:
        BASE_DIR = Path(__file__).resolve().parents[3]

        result = run_discovery_scan(
            base_dir=BASE_DIR,
            org_id=request.org_id,
            site_id=request.site_id,
            subnet=request.subnet,
            start_ip=request.start_ip,
            end_ip=request.end_ip,
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------------------------
# 2️⃣ LIST SCAN HISTORY
# -------------------------------------------------

@router.get("/history")
def list_scan_history(org_id: str, site_id: str):

    BASE_DIR = Path(__file__).resolve().parents[3]

    discovery_root = get_discovery_root(
        BASE_DIR, org_id, site_id
    )

    if not discovery_root.exists():
        return {
            "org_id": org_id,
            "site_id": site_id,
            "total_scans": 0,
            "scans": []
        }

    scans = sorted(
        [d.name for d in discovery_root.iterdir() if d.is_dir()],
        reverse=True
    )

    return {
        "org_id": org_id,
        "site_id": site_id,
        "total_scans": len(scans),
        "scans": scans
    }


# -------------------------------------------------
# 3️⃣ GET SCAN RESULTS
# -------------------------------------------------

@router.get("/results")
def get_scan_results(org_id: str, site_id: str, scan_id: str):

    BASE_DIR = Path(__file__).resolve().parents[3]

    discovery_root = get_discovery_root(
        BASE_DIR, org_id, site_id
    )

    if not discovery_root.exists():
        raise HTTPException(
            status_code=404,
            detail="No discovery history found"
        )

    scan_path = discovery_root / scan_id

    if not scan_path.exists():
        available = sorted(
            [d.name for d in discovery_root.iterdir() if d.is_dir()],
            reverse=True
        )

        raise HTTPException(
            status_code=404,
            detail={
                "message": f"Scan '{scan_id}' not found",
                "available_scans": available
            }
        )

    result_file = scan_path / "scan_results.json"

    if not result_file.exists():
        raise HTTPException(
            status_code=500,
            detail="Scan folder exists but result file missing"
        )

    with open(result_file, "r") as f:
        return json.load(f)

# -------------------------------------------------
# 4️⃣ APPROVE & REGISTER DEVICE
# -------------------------------------------------

class DiscoveryDecisionRequest(BaseModel):
    org_id: str
    site_id: str
    scan_id: str
    decision: str  # approve / discard


@router.post("/decision")
def discovery_decision(request: DiscoveryDecisionRequest):

    BASE_DIR = Path(__file__).resolve().parents[3]

    discovery_root = get_discovery_root(
        BASE_DIR, request.org_id, request.site_id
    )

    scan_path = discovery_root / request.scan_id

    if not scan_path.exists():
        raise HTTPException(status_code=404, detail="Scan not found")

    metadata_file = scan_path / "scan_metadata.json"

    if not metadata_file.exists():
        raise HTTPException(status_code=500, detail="Metadata missing")

    with open(metadata_file, "r") as f:
        metadata = json.load(f)

    if metadata["status"] in ["APPROVED", "DISCARDED"]:
        raise HTTPException(
            status_code=400,
            detail=f"Scan already {metadata['status']}"
        )

    if metadata["status"] != "COMPLETED":
        raise HTTPException(
            status_code=400,
            detail=f"Scan cannot be processed. Current status: {metadata['status']}"
        )
    # -------------------------------------------------
    # DISCARD
    # -------------------------------------------------
    if request.decision.lower() == "discard":

        metadata["status"] = "DISCARDED"

        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=4)

        return {
            "status": "DISCARDED",
            "scan_id": request.scan_id
        }

    # -------------------------------------------------
    # APPROVE
    # -------------------------------------------------
    if request.decision.lower() == "approve":

        result_file = scan_path / "scan_results.json"

        with open(result_file, "r") as f:
            scan_results = json.load(f)

        registry_path = (
            BASE_DIR
            / "data"
            / "orgs"
            / request.org_id
            / "sites"
            / request.site_id
            / "device_registry.json"
        )

        devices = []
        if registry_path.exists():
            with open(registry_path, "r") as f:
                devices = json.load(f)

        next_id = len(devices) + 1
        registered = 0

        for entry in scan_results:

            ssh = entry.get("ssh_open", False)
            telnet = entry.get("telnet_open", False)

            if not ssh and not telnet:
                continue

            if ssh and telnet:
                protocol = "both"
            elif ssh:
                protocol = "ssh"
            else:
                protocol = "telnet"

            # Skip already registered IPs
            if any(d["mgmt_ip"] == entry["ip"] for d in devices):
                continue


            def utc_now():
                return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

            device_id = str(uuid.uuid4())
            now = utc_now()

            devices.append({
                "device_id": device_id,
                "mgmt_ip": entry["ip"],
                "protocol": protocol,
                "vendor": "unknown",
                "hostname": None,
                "status": "ACTIVE",
                "created_at": now,
                "updated_at": now,
                "last_seen_at": None,
                "last_backup_at": None,
                "last_command_at": None
            })
            registered += 1
            
        with open(registry_path, "w") as f:
            json.dump(devices, f, indent=4)

        metadata["status"] = "APPROVED"

        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=4)

        return {
            "status": "APPROVED",
            "registered_devices": registered
        }

    raise HTTPException(
        status_code=400,
        detail="Decision must be 'approve' or 'discard'"
    )
