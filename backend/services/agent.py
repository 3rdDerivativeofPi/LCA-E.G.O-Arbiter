from .parser import parse_cv, parse_jd
from .embedder import embed_cv, embed_jd
from .matcher import compute_score
from .explainer import explain
from .bias_detector import detect_bias


async def run_pipeline(
    cv_bytes: bytes,
    cv_filename: str,
    jd_text: str,
    weights: dict | None = None,
) -> dict:

    # === OBSERVE ===
    cv = await parse_cv(cv_bytes, cv_filename)
    jd = await parse_jd(jd_text)

    # === ANALYZE ===
    cv_emb = await embed_cv(cv)
    jd_emb = await embed_jd(jd)
    score = compute_score(cv_emb, jd_emb, weights)

    # === DECIDE ===
    explanation = await explain(cv, jd, score)

    # === REFLECT ===
    bias_report = await detect_bias(jd_text)

    # === ADJUST ===
    flags = []
    if score["breakdown"]["skills"] < 30:
        flags.append("Low skill alignment — consider revising the JD or sourcing differently.")
    if bias_report["bias_score"] > 60:
        flags.append("High bias score detected in JD — review flagged phrases before publishing.")

    return {
        "candidate": cv.get("name", "Unknown"),
        "score": score,
        "explanation": explanation,
        "bias_report": bias_report,
        "agent_flags": flags,
        "parsed_cv": cv,
        "parsed_jd": jd,
        "cv_embeddings": cv_emb,
        "jd_embeddings": jd_emb,
    }