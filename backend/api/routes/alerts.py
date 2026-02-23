# backend/api/routes/alerts.py

from fastapi import APIRouter
import json
from pathlib import Path
from datetime import datetime

router = APIRouter()


@router.get("/alerts/{org_id}/{site_id}")
def get_alerts(org_id: str, site_id: str):

    base_dir = Path.cwd()

    today = datetime.now().strftime("%d-%m-%Y")

    path = (
        base_dir
        / "data"
        / "orgs"
        / org_id
        / "sites"
        / site_id
        / "alerts"
        / f"{today}.json"
    )

    if not path.exists():
        return []

    return json.loads(path.read_text())