from .llm_client import llm

SYSTEM = (
    "You are an objective HR analyst. "
    "Write in professional, concise bullet points. "
    "Return ONLY valid JSON, no markdown fences."
)


async def explain(cv: dict, jd: dict, score: dict) -> dict:
    prompt = f"""
Analyze this candidate against the job description. Be concise.

CANDIDATE: {cv}
JOB: {jd}
SCORES: {score}

Return ONLY this JSON, no extra text:
{{
  "strengths": ["max 3 short bullets"],
  "weaknesses": ["max 3 short bullets"],
  "overall_fit": "one sentence only",
  "recommendation": "Strongly Recommended | Recommended | Consider | Not Recommended"
}}
"""
    return await llm.generate_json(prompt, SYSTEM)