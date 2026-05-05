from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.session_store import session_store
from services.parser import parse_cv, parse_jd
from services.embedder import embed_cv, embed_jd
from services.matcher import compute_score
import json

router = APIRouter()


@router.post("/session")
async def create_session(jd_text: str = Form(...)):
    """Create a new ranking session with a job description."""
    try:
        session = session_store.create()
        parsed_jd = await parse_jd(jd_text)
        jd_emb = await embed_jd(parsed_jd)

        session.jd_text = jd_text
        session.parsed_jd = parsed_jd
        session.jd_embeddings = jd_emb

        return {
            "success": True,
            "session_id": session.session_id,
            "parsed_jd": parsed_jd,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/session/{session_id}/cv")
async def upload_cv(session_id: str, cv_file: UploadFile = File(...)):
    """Upload a single CV to an existing session."""
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    try:
        cv_bytes = await cv_file.read()
        parsed_cv = await parse_cv(cv_bytes, cv_file.filename)
        cv_emb = await embed_cv(parsed_cv)
        candidate_id = session.add_candidate(
            parsed_cv.get("name", cv_file.filename),
            parsed_cv,
            cv_emb,
        )
        return {
            "success": True,
            "candidate_id": candidate_id,
            "name": parsed_cv.get("name", "Unknown"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{session_id}/rank")
async def rank_candidates(session_id: str, weights: str = None):
    """Score and rank all candidates in a session."""
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    if not session.candidates:
        raise HTTPException(status_code=400, detail="No candidates uploaded yet.")

    try:
        w = json.loads(weights) if weights else None
        leaderboard = []
        for c in session.candidates:
            score = compute_score(c["cv_embeddings"], session.jd_embeddings, w)
            leaderboard.append({
                "id": c["id"],
                "name": c["name"],
                "score": score,
            })

        leaderboard.sort(key=lambda x: x["score"]["total"], reverse=True)
        for i, entry in enumerate(leaderboard):
            entry["rank"] = i + 1

        return {"success": True, "leaderboard": leaderboard}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/session/{session_id}/explain/{candidate_id}")
async def explain_candidate(session_id: str, candidate_id: str):
    """Explain a specific candidate on demand."""
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    candidate = next((c for c in session.candidates if c["id"] == candidate_id), None)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found.")

    try:
        from services.explainer import explain
        from services.matcher import compute_score
        score = compute_score(candidate["cv_embeddings"], session.jd_embeddings)
        explanation = await explain(candidate["parsed_cv"], session.parsed_jd, score)
        return {"success": True, "explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))