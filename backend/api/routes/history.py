# backend/api/routes/history.py

from fastapi import APIRouter, HTTPException
from pathlib import Path
import json

router = APIRouter()


# -------------------------------------------------
# VALIDATE ORG + SITE
# -------------------------------------------------
def validate_org_site(base_dir: Path, org_id: str, site_id: str):

    org_path = base_dir / "data" / "orgs" / org_id
    if not org_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Organization '{org_id}' not found"
        )

    site_path = org_path / "sites" / site_id
    if not site_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Site '{site_id}' not found under org '{org_id}'"
        )

    return site_path


# -------------------------------------------------
# GET HISTORY ROOT
# -------------------------------------------------
def get_history_root(base_dir: Path, org_id: str, site_id: str, module: str):

    site_path = validate_org_site(base_dir, org_id, site_id)

    history_root = site_path / module / "history"

    if not history_root.exists():
        return None

    return history_root


# -------------------------------------------------
# 1️⃣ LIST RUNS
# -------------------------------------------------
@router.get("/config-backup/runs")
def list_runs(org_id: str, site_id: str):

    BASE_DIR = Path(__file__).resolve().parents[3]

    history_root = get_history_root(
        BASE_DIR, org_id, site_id, "config_backup"
    )

    if not history_root:
        return {
            "org_id": org_id,
            "site_id": site_id,
            "total_runs": 0,
            "runs": []
        }

    runs = sorted(
        [d.name for d in history_root.iterdir() if d.is_dir()],
        reverse=True
    )

    return {
        "org_id": org_id,
        "site_id": site_id,
        "total_runs": len(runs),
        "runs": runs
    }


# -------------------------------------------------
# 2️⃣ GET RUN SUMMARY
# -------------------------------------------------
@router.get("/config-backup/summary")
def get_run_summary(org_id: str, site_id: str, run_id: str):

    BASE_DIR = Path(__file__).resolve().parents[3]

    history_root = get_history_root(
        BASE_DIR, org_id, site_id, "config_backup"
    )

    if not history_root:
        raise HTTPException(
            status_code=404,
            detail="No execution history found for this site"
        )

    run_path = history_root / run_id

    if not run_path.exists():
        available_runs = sorted(
            [d.name for d in history_root.iterdir() if d.is_dir()],
            reverse=True
        )

        raise HTTPException(
            status_code=404,
            detail={
                "message": f"Run '{run_id}' not found",
                "available_runs": available_runs
            }
        )

    summary_file = run_path / "run_summary.json"

    if not summary_file.exists():
        raise HTTPException(
            status_code=500,
            detail="Run folder exists but summary file is missing"
        )

    with open(summary_file, "r") as f:
        return json.load(f)


# -------------------------------------------------
# 3️⃣ GET DEVICE RESULTS
# -------------------------------------------------
@router.get("/config-backup/device-results")
def get_device_results(org_id: str, site_id: str, run_id: str):

    BASE_DIR = Path(__file__).resolve().parents[3]

    history_root = get_history_root(
        BASE_DIR, org_id, site_id, "config_backup"
    )

    if not history_root:
        raise HTTPException(
            status_code=404,
            detail="No execution history found for this site"
        )

    run_path = history_root / run_id

    if not run_path.exists():
        available_runs = sorted(
            [d.name for d in history_root.iterdir() if d.is_dir()],
            reverse=True
        )

        raise HTTPException(
            status_code=404,
            detail={
                "message": f"Run '{run_id}' not found",
                "available_runs": available_runs
            }
        )

    result_file = run_path / "device_results.json"

    if not result_file.exists():
        raise HTTPException(
            status_code=500,
            detail="Run folder exists but device_results.json is missing"
        )

    with open(result_file, "r") as f:
        return json.load(f)
