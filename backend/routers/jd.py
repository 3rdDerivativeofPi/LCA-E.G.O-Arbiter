from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.jd_generator import generate_jd

router = APIRouter()


class JDGenerateRequest(BaseModel):
    title: str
    company: str = ""
    location: str = ""
    work_type: str = ""
    required_skills: list[str] = []
    preferred_skills: list[str] = []
    experience_required: str = ""
    education_required: str = ""
    responsibilities: str = ""
    perks: str = ""


@router.post("/generate")
async def generate_job_description(payload: JDGenerateRequest):
    try:
        result = await generate_jd(payload.model_dump())
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
