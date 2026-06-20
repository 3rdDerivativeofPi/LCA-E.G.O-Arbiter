from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.session_store import session_store
from services.matcher import compute_score
from services.explainer import explain
from services.email_generator import generate_email

router = APIRouter()


class EmailGenerateRequest(BaseModel):
    email_type: str  # "invite" or "reject"
    company_name: str = ""
    sender_name: str = ""
    interview_details: str = ""


@router.post("/session/{session_id}/candidate/{candidate_id}")
async def generate_candidate_email(
    session_id: str,
    candidate_id: str,
    payload: EmailGenerateRequest,
):
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    candidate = next((c for c in session.candidates if c["id"] == candidate_id), None)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found.")

    if payload.email_type not in ("invite", "reject"):
        raise HTTPException(status_code=400, detail="email_type must be 'invite' or 'reject'.")

    try:
        score = compute_score(candidate["cv_embeddings"], session.jd_embeddings)
        explanation = await explain(candidate["parsed_cv"], session.parsed_jd, score)

        email = await generate_email(
            email_type=payload.email_type,
            cv=candidate["parsed_cv"],
            jd=session.parsed_jd,
            score=score,
            explanation=explanation,
            company_name=payload.company_name,
            sender_name=payload.sender_name,
            interview_details=payload.interview_details,
        )
        return {"success": True, "data": email}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
