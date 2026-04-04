from .llm_client import llm

SYSTEM = (
    "You are an objective HR analyst. "
    "Write in professional, concise bullet points. "
    "Return ONLY valid JSON, no markdown fences."
)


async def explain(cv: dict, jd: dict, score: dict) -> dict:
    prompt = f"""
Given the candidate profile and job description below, provide an explainability report.

CANDIDATE: {cv}
JOB DESCRIPTION: {jd}
MATCH SCORES: {score}

Return JSON with exactly these keys:
{{
  "strengths": ["bullet 1", "bullet 2"],
  "weaknesses": ["bullet 1", "bullet 2"],
  "overall_fit": "2-3 sentence summary",
  "recommendation": "Strongly Recommended | Recommended | Consider | Not Recommended"
}}
"""
    return await llm.generate_json(prompt, SYSTEM)