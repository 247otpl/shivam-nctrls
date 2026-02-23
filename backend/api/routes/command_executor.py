# backend/api/routes/command_executor.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
from fastapi.responses import StreamingResponse
import json
import queue
import threading

from backend.modules.command_executor.service import run_command_executor
from backend.core.job_manager import job_manager

router = APIRouter()


# -------------------------------------------------
# REQUEST MODEL
# -------------------------------------------------
class CommandExecutionRequest(BaseModel):
    org_id: str
    site_id: str
    mode: str = "all"
    device_ids: list[str] | None = None
    mgmt_ips: list[str] | None = None
    dry_run: bool = False


# -------------------------------------------------
# NORMAL EXECUTION (Non-streaming)
# -------------------------------------------------
@router.post("/run")
def run_executor(request: CommandExecutionRequest):

    try:
        BASE_DIR = Path(__file__).resolve().parents[3]

        result = run_command_executor(
            base_dir=BASE_DIR,
            org_id=request.org_id,
            site_id=request.site_id,
            mode=request.mode,
            device_ids=request.device_ids,
            mgmt_ips=request.mgmt_ips,
            dry_run=request.dry_run,
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------------------------
# LIVE STREAM EXECUTION (Parallel + Real-time)
# -------------------------------------------------
@router.post("/run-stream")
def run_executor_stream(request: CommandExecutionRequest):

    BASE_DIR = Path(__file__).resolve().parents[3]

    event_queue = queue.Queue()

    # ---------------------------------------------
    # Background execution thread
    # ---------------------------------------------
    def background_run():
        try:
            run_command_executor(
                base_dir=BASE_DIR,
                org_id=request.org_id,
                site_id=request.site_id,
                mode=request.mode,
                device_ids=request.device_ids,
                mgmt_ips=request.mgmt_ips,
                dry_run=request.dry_run,
                event_queue=event_queue,
            )
        except Exception as e:
            event_queue.put({
                "type": "error",
                "message": str(e)
            })

    thread = threading.Thread(target=background_run)
    thread.start()

    # ---------------------------------------------
    # Streaming generator
    # ---------------------------------------------
    def event_stream():
        while True:
            event = event_queue.get()

            yield json.dumps(event) + "\n"

            # Stop when execution completes
            if event.get("type") == "complete":
                break

            if event.get("type") == "error":
                break

    return StreamingResponse(
        event_stream(),
        media_type="application/json"
    )

@router.post("/cancel/{run_id}")
def cancel_job(run_id: str):

    job_manager.cancel_job(run_id)

    return {
        "message": f"Run {run_id} cancellation requested"
    }

@router.get("/progress/{run_id}")
def get_progress(run_id: str):

    status = job_manager.get_status(run_id)

    if not status:
        raise HTTPException(status_code=404, detail="Run not found")

    return status
