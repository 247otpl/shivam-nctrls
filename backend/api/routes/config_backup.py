# backend/api/routes/config_backup.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
from typing import List, Optional

from backend.modules.config_backup.service import run_config_backup

router = APIRouter()


# -------------------------------------------------
# REQUEST MODEL
# -------------------------------------------------
class BackupRequest(BaseModel):
    org_id: str
    site_id: Optional[str] = None
    mode: str = "site"  # safer default
    device_ids: Optional[List[str]] = None
    mgmt_ips: Optional[List[str]] = None


# -------------------------------------------------
# ROUTE
# -------------------------------------------------
@router.post("/run")
def execute_config_backup(request: BackupRequest):

    BASE_DIR = Path(__file__).resolve().parents[3]

    # -------------------------------------------------
    # VALIDATIONS
    # -------------------------------------------------

    allowed_modes = {"site", "all", "device_ids", "mgmt_ips"}

    if request.mode not in allowed_modes:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid mode. Allowed: {allowed_modes}"
        )

    # Enforce site_id for site mode
    if request.mode == "site" and not request.site_id:
        raise HTTPException(
            status_code=400,
            detail="site_id is required when mode='site'"
        )

    # device_ids validation
    if request.mode == "device_ids":
        if not request.device_ids:
            raise HTTPException(
                status_code=400,
                detail="device_ids required when mode='device_ids'"
            )

    # mgmt_ips validation
    if request.mode == "mgmt_ips":
        if not request.mgmt_ips:
            raise HTTPException(
                status_code=400,
                detail="mgmt_ips required when mode='mgmt_ips'"
            )

    try:
        result = run_config_backup(
            base_dir=BASE_DIR,
            org_id=request.org_id,
            site_id=request.site_id,
            mode=request.mode,
            device_ids=request.device_ids,
            mgmt_ips=request.mgmt_ips,
        )

        return result

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
