from sentence_transformers import SentenceTransformer

_model = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("AITeamVN/Vietnamese_Embedding")
        _model.max_seq_length = 2048
    return _model


def _safe_text(text: str) -> str:
    return text.strip() if text.strip() else "none"


def _embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_model()
    vectors = model.encode(texts, normalize_embeddings=True)
    return [v.tolist() for v in vectors]


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
    vectors = _embed_texts([
        _safe_text(skills_text),
        _safe_text(experience_text),
        _safe_text(education_text),
    ])
    return {"skills": vectors[0], "experience": vectors[1], "education": vectors[2]}


async def embed_jd(jd: dict) -> dict:
    skills_text = ", ".join(jd.get("required_skills", []) + jd.get("preferred_skills", []))
    experience_text = jd.get("experience_required", "")
    education_text = jd.get("education_required", "")
    vectors = _embed_texts([
        _safe_text(skills_text),
        _safe_text(experience_text),
        _safe_text(education_text),
    ])
    return {"skills": vectors[0], "experience": vectors[1], "education": vectors[2]}