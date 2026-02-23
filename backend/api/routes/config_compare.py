# backend/api/routes/config_compare.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path

from backend.modules.config_compare.service import compare_config_files

router = APIRouter()


class CompareRequest(BaseModel):
    file1: str
    file2: str


@router.post("/compare")
def compare_configs(request: CompareRequest):

    try:
        file1 = Path(request.file1)
        file2 = Path(request.file2)

        result = compare_config_files(file1, file2)

        return {
            "file1": request.file1,
            "file2": request.file2,
            "total_lines": len(result),
            "diff": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
