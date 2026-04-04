import asyncio
from services.embedder import embed_jd

async def test():
    jd = {
        "required_skills": ["Python", "FastAPI", "PostgreSQL"],
        "preferred_skills": ["Docker", "Redis"],
        "experience_required": "3+ years",
        "education_required": "Bachelor's in Computer Science"
    }
    result = await embed_jd(jd)
    for field, vector in result.items():
        print(f"{field}: {len(vector)} dimensions, first 3 values: {vector[:3]}")

asyncio.run(test())