from .llm_client import llm

SYSTEM = (
    "You are a DEI (Diversity, Equity, Inclusion) compliance auditor. "
    "Return ONLY valid JSON, no markdown fences."
)


async def detect_bias(jd_text: str) -> dict:
    prompt = f"""
Analyse the job description below for biased or exclusionary language.
Look for: gendered words, age-coded language, unrealistic experience requirements,
unnecessary degree requirements, cultural/geographic bias.

JOB DESCRIPTION:
{jd_text[:3000]}

Return JSON with exactly these keys:
{{
  "bias_score": 0-100,
  "flags": [
    {{"phrase": "...", "issue": "...", "suggestion": "..."}}
  ],
  "overall_assessment": "string",
  "improved_excerpt": "rewritten version of the most problematic section"
}}
"""
    return await llm.generate_json(prompt, SYSTEM)