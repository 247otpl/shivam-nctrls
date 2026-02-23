# backend/api/routes/provisioning.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
import json
import uuid
from datetime import datetime, timezone


router = APIRouter()


# -------------------------------------------------
# UTILITIES
# -------------------------------------------------

def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def get_registry_path(base_dir: Path, org_id: str, site_id: str) -> Path:
    return (
        base_dir
        / "data"
        / "orgs"
        / org_id
        / "sites"
        / site_id
        / "device_registry.json"
    )


def load_registry(base_dir: Path, org_id: str, site_id: str):

    registry_path = get_registry_path(base_dir, org_id, site_id)

    if not registry_path.exists():
        return []

    with open(registry_path, "r") as f:
        return json.load(f)


def save_registry(base_dir: Path, org_id: str, site_id: str, devices):

    registry_path = get_registry_path(base_dir, org_id, site_id)

    registry_path.parent.mkdir(parents=True, exist_ok=True)

    with open(registry_path, "w") as f:
        json.dump(devices, f, indent=4)


def build_device_record(
    mgmt_ip: str,
    protocol: str,
    vendor: str = "unknown",
    hostname: str = None,
):
    now = utc_now()

    return {
        "device_id": str(uuid.uuid4()),
        "mgmt_ip": mgmt_ip,
        "protocol": protocol,
        "vendor": vendor,
        "hostname": hostname,
        "status": "ACTIVE",
        "created_at": now,
        "updated_at": now,
        "last_seen_at": None,
        "last_backup_at": None,
        "last_command_at": None,
    }


# -------------------------------------------------
# MODELS
# -------------------------------------------------

class DeviceCreateRequest(BaseModel):
    org_id: str
    site_id: str
    mgmt_ip: str
    protocol: str
    vendor: str | None = "unknown"
    hostname: str | None = None


class DeviceUpdateRequest(BaseModel):
    org_id: str
    site_id: str
    device_id: str
    protocol: str | None = None
    vendor: str | None = None
    hostname: str | None = None
    status: str | None = None


class DeviceDeleteRequest(BaseModel):
    org_id: str
    site_id: str
    device_id: str


# -------------------------------------------------
# ADD DEVICE
# -------------------------------------------------

@router.post("/add")
def add_device(request: DeviceCreateRequest):

    BASE_DIR = Path(__file__).resolve().parents[3]

    devices = load_registry(BASE_DIR, request.org_id, request.site_id)

    # Prevent duplicate mgmt_ip
    if any(d["mgmt_ip"] == request.mgmt_ip for d in devices):
        raise HTTPException(
            status_code=400,
            detail="Device with this mgmt_ip already exists"
        )

    new_device = build_device_record(
        mgmt_ip=request.mgmt_ip,
        protocol=request.protocol,
        vendor=request.vendor or "unknown",
        hostname=request.hostname,
    )

    devices.append(new_device)

    save_registry(BASE_DIR, request.org_id, request.site_id, devices)

    return {
        "status": "SUCCESS",
        "device_id": new_device["device_id"]
    }


# -------------------------------------------------
# UPDATE DEVICE
# -------------------------------------------------

@router.put("/update")
def update_device(request: DeviceUpdateRequest):

    BASE_DIR = Path(__file__).resolve().parents[3]

    devices = load_registry(BASE_DIR, request.org_id, request.site_id)

    for device in devices:

        if device["device_id"] == request.device_id:

            if request.protocol is not None:
                device["protocol"] = request.protocol

            if request.vendor is not None:
                device["vendor"] = request.vendor

            if request.hostname is not None:
                device["hostname"] = request.hostname

            if request.status is not None:
                device["status"] = request.status

            device["updated_at"] = utc_now()

            save_registry(BASE_DIR, request.org_id, request.site_id, devices)

            return {"status": "UPDATED"}

    raise HTTPException(
        status_code=404,
        detail="Device not found"
    )


# -------------------------------------------------
# DELETE DEVICE (Soft Delete)
# -------------------------------------------------

@router.delete("/delete")
def delete_device(request: DeviceDeleteRequest):

    BASE_DIR = Path(__file__).resolve().parents[3]

    devices = load_registry(BASE_DIR, request.org_id, request.site_id)

    for device in devices:

        if device["device_id"] == request.device_id:

            device["status"] = "DECOMMISSIONED"
            device["updated_at"] = utc_now()

            save_registry(BASE_DIR, request.org_id, request.site_id, devices)

            return {"status": "DECOMMISSIONED"}

    raise HTTPException(
        status_code=404,
        detail="Device not found"
    )


# -------------------------------------------------
# LIST DEVICES
# -------------------------------------------------

@router.get("/list")
def list_devices(org_id: str, site_id: str):

    BASE_DIR = Path(__file__).resolve().parents[3]

    devices = load_registry(BASE_DIR, org_id, site_id)

    return {
        "org_id": org_id,
        "site_id": site_id,
        "total_devices": len(devices),
        "devices": devices
    }