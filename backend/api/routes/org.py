# backend/api/routes/org.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path

from backend.core.bootstrap import bootstrap_org, bootstrap_site

router = APIRouter()


# -------------------------------------------------
# MODELS
# -------------------------------------------------

class OrgCreateRequest(BaseModel):
    org_id: str
    org_name: str


class SiteCreateRequest(BaseModel):
    org_id: str
    site_id: str
    site_name: str


# -------------------------------------------------
# CREATE ORG
# -------------------------------------------------

@router.post("/create")
def create_org(request: OrgCreateRequest):

    BASE_DIR = Path(__file__).resolve().parents[3]

    try:
        bootstrap_org(BASE_DIR, request.org_id, request.org_name)

        return {
            "status": "SUCCESS",
            "message": f"Organization {request.org_id} created"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------------------------
# CREATE SITE
# -------------------------------------------------

@router.post("/site/create")
def create_site(request: SiteCreateRequest):

    BASE_DIR = Path(__file__).resolve().parents[3]

    try:
        bootstrap_site(
            BASE_DIR,
            request.org_id,
            request.site_id,
            request.site_name
        )

        return {
            "status": "SUCCESS",
            "message": f"Site {request.site_id} created under {request.org_id}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
