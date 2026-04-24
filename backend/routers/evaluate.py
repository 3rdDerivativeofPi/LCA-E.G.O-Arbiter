from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from ..services.agent import run_pipeline
import json
import traceback

router = APIRouter()


@router.post("/")
async def evaluate_candidate(
    cv_file: UploadFile = File(...),
    jd_text: str = Form(...),
    weights: str = Form(None),
):
    try:
        w = json.loads(weights) if weights else None
        cv_bytes = await cv_file.read()
        result = await run_pipeline(cv_bytes, cv_file.filename, jd_text, w)
        return {"success": True, "data": result}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))