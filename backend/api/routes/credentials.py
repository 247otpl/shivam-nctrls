# backend/api/routes/credentials.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path

from backend.core.credentials import save_credentials

router = APIRouter()


# -------------------------------------------------
# MODEL
# -------------------------------------------------
class CredentialRequest(BaseModel):
    org_id: str
    site_id: str
    module: str  # "config_backup" or "command_executor"
    username: str
    password: str


# -------------------------------------------------
# SET CREDENTIALS
# -------------------------------------------------
@router.post("/set")
def set_credentials(request: CredentialRequest):

    try:
        if request.module not in [
            "config_backup",
            "command_executor",
        ]:
            raise ValueError(
                "Module must be 'config_backup' or 'command_executor'"
            )

        BASE_DIR = Path(__file__).resolve().parents[3]

        cred_dir = (
            BASE_DIR
            / "data"
            / "orgs"
            / request.org_id
            / "sites"
            / request.site_id
            / request.module
            / "credentials"
        )

        # Validate org/site existence
        if not cred_dir.parent.exists():
            raise FileNotFoundError(
                "Org/Site/Module structure not found. Create org/site first."
            )

        save_credentials(
            cred_dir=cred_dir,
            username=request.username,
            password=request.password,
            base_dir=BASE_DIR,
        )

        return {
            "status": "credentials_saved",
            "org_id": request.org_id,
            "site_id": request.site_id,
            "module": request.module,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
