# backend/api/routes/command_executor_history.py

from fastapi import APIRouter, HTTPException
from pathlib import Path
import json

router = APIRouter()


@router.get("/summary")
def get_executor_summary(
    org_id: str,
    site_id: str,
    run_id: str,
):

    BASE_DIR = Path(__file__).resolve().parents[3]

    history_file = (
        BASE_DIR
        / "data"
        / "orgs"
        / org_id
        / "sites"
        / site_id
        / "command_executor"
        / "history"
        / run_id
        / "summary.json"
    )

    if not history_file.exists():
        raise HTTPException(status_code=404, detail="Run not found")

    return json.loads(history_file.read_text())


@router.get("/runs")
def list_executor_runs(org_id: str, site_id: str):

    BASE_DIR = Path(__file__).resolve().parents[3]

    history_dir = (
        BASE_DIR
        / "data"
        / "orgs"
        / org_id
        / "sites"
        / site_id
        / "command_executor"
        / "history"
    )

    if not history_dir.exists():
        return {"runs": []}

    runs = sorted(
        [d.name for d in history_dir.iterdir() if d.is_dir()],
        reverse=True
    )

    return {"runs": runs}
