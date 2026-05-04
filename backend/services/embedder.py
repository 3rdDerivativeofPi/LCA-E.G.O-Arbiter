from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-mpnet-base-v2")


def _safe_text(text: str) -> str:
    return text.strip() if text.strip() else "none"


def _embed(text: str) -> list[float]:
    return _model.encode(text, normalize_embeddings=True).tolist()


async def embed_cv(cv: dict) -> dict:
    skills_text = ", ".join(cv.get("skills", []))
    experience_text = " | ".join(
        f"{e.get('title','')} at {e.get('company','')} ({e.get('duration','')}) — {e.get('description','')}"
        for e in cv.get("experience", [])
    )
    education_text = " | ".join(
        f"{e.get('degree','')} from {e.get('institution','')} ({e.get('year','')})"
        for e in cv.get("education", [])
    )
    return {
        "skills":     _embed(_safe_text(skills_text)),
        "experience": _embed(_safe_text(experience_text)),
        "education":  _embed(_safe_text(education_text)),
    }


async def embed_jd(jd: dict) -> dict:
    skills_text = ", ".join(jd.get("required_skills", []) + jd.get("preferred_skills", []))
    experience_text = jd.get("experience_required", "")
    education_text = jd.get("education_required", "")
    return {
        "skills":     _embed(_safe_text(skills_text)),
        "experience": _embed(_safe_text(experience_text)),
        "education":  _embed(_safe_text(education_text)),
    }