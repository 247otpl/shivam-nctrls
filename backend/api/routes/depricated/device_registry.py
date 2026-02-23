# backend/api/routes/device_registry.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
from typing import Optional

from backend.core.device_registry import DeviceRegistry

router = APIRouter()


# -----------------------------
# REQUEST MODELS
# -----------------------------

class CreateClientRequest(BaseModel):
    client_id: str
    client_name: str


class AddDeviceRequest(BaseModel):
    client_id: str
    device_id: str
    vendor: str
    model: str
    mgmt_ip: str
    protocol: str = "ssh"
    location: Optional[str] = ""
    notes: Optional[str] = ""


# -----------------------------
# CREATE CLIENT
# -----------------------------

@router.post("/clients/create")
def create_client(request: CreateClientRequest):
    try:
        BASE_DIR = Path(__file__).resolve().parents[3]
        registry = DeviceRegistry(BASE_DIR)

        registry.create_client(
            client_id=request.client_id,
            client_name=request.client_name
        )

        return {
            "status": "client_created",
            "client_id": request.client_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# ADD DEVICE
# -----------------------------

@router.post("/devices/add")
def add_device(request: AddDeviceRequest):
    try:
        BASE_DIR = Path(__file__).resolve().parents[3]
        registry = DeviceRegistry(BASE_DIR)

        registry.add_device(
            client_id=request.client_id,
            device_id=request.device_id,
            vendor=request.vendor,
            model=request.model,
            mgmt_ip=request.mgmt_ip,
            protocol=request.protocol,
            location=request.location,
            notes=request.notes
        )

        return {
            "status": "device_added",
            "device_id": request.device_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# LIST DEVICES
# -----------------------------

@router.get("/devices/list/{client_id}")
def list_devices(client_id: str):
    try:
        BASE_DIR = Path(__file__).resolve().parents[3]
        registry = DeviceRegistry(BASE_DIR)

        devices = registry.get_devices(client_id)

        return {
            "client_id": client_id,
            "total_devices": len(devices),
            "devices": devices
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
