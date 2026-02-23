# backend/api/routes/modules.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.core.context import ExecutionContext
from backend.modules.config_backup.service import run_config_backup
from backend.modules.command_executor.service import run_command_execution

from pathlib import Path

router = APIRouter()


# --------------------------------------------
# Request Model
# --------------------------------------------
class ModuleRequest(BaseModel):
    org_id: str
    site_id: str


# --------------------------------------------
# CONFIG BACKUP
# --------------------------------------------
@router.post("/config-backup/run")
def run_backup(req: ModuleRequest):
    try:
        ctx = ExecutionContext(
            org_id=req.org_id,
            site_id=req.site_id,
        )

        result = run_config_backup(ctx)
        return {"message": "Config Backup Completed", "result": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------------------------------------------
# COMMAND EXECUTION
# --------------------------------------------
@router.post("/command-exec/run")
def run_commands(req: ModuleRequest):
    try:
        ctx = ExecutionContext(
            org_id=req.org_id,
            site_id=req.site_id,
        )

        result = run_command_execution(ctx)
        return {"message": "Command Execution Completed", "result": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
