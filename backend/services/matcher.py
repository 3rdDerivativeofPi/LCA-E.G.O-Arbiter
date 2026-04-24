import numpy as np
from ..config import DEFAULT_WEIGHTS


def cosine_similarity(a: list[float], b: list[float]) -> float:
    va, vb = np.array(a), np.array(b)
    denom = np.linalg.norm(va) * np.linalg.norm(vb)
    return float(np.dot(va, vb) / denom) if denom > 0 else 0.0


def compute_score(cv_embeddings: dict, jd_embeddings: dict, weights: dict | None = None) -> dict:
    w = weights or DEFAULT_WEIGHTS
    skills_sim     = cosine_similarity(cv_embeddings["skills"],     jd_embeddings["skills"])
    experience_sim = cosine_similarity(cv_embeddings["experience"], jd_embeddings["experience"])
    education_sim  = cosine_similarity(cv_embeddings["education"],  jd_embeddings["education"])

    total = (
        skills_sim     * w["skills"] +
        experience_sim * w["experience"] +
        education_sim  * w["education"]
    )
    return {
        "total": round(total * 100, 2),
        "breakdown": {
            "skills":     round(skills_sim * 100, 2),
            "experience": round(experience_sim * 100, 2),
            "education":  round(education_sim * 100, 2),
        },
        "weights_used": w,
    }