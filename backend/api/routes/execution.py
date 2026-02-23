from fastapi import APIRouter, HTTPException
from backend.core.context import ExecutionContext
from backend.core.execution_tracker import ExecutionTracker

router = APIRouter()


@router.get("/execution/{module}")
def get_last_execution(module: str, org_id: str, site_id: str):
    try:
        ctx = ExecutionContext(org_id, site_id)
        ctx.validate()

        module_dir = ctx.paths.module_dir(
            org_id,
            site_id,
            module,
        )

        tracker = ExecutionTracker(module_dir)

        return tracker.get_last_run()

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/execution/{module}/history")
def get_execution_history(module: str, org_id: str, site_id: str):
    try:
        ctx = ExecutionContext(org_id, site_id)
        ctx.validate()

        module_dir = ctx.paths.module_dir(
            org_id,
            site_id,
            module,
        )

        tracker = ExecutionTracker(module_dir)

        return tracker.get_all_runs()

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
