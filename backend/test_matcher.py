import asyncio
from services.embedder import embed_cv, embed_jd
from services.matcher import compute_score

async def test():
    cv = {
        "skills": ["Python", "FastAPI", "PostgreSQL"],
        "experience": [{"title": "Backend Developer", "company": "Acme", "duration": "2 years", "description": "Built REST APIs"}],
        "education": [{"degree": "Bachelor's in Computer Science", "institution": "Hanoi University", "year": "2022"}]
    }
    jd = {
        "required_skills": ["Python", "FastAPI", "PostgreSQL"],
        "preferred_skills": ["Docker", "Redis"],
        "experience_required": "3+ years",
        "education_required": "Bachelor's in Computer Science"
    }

    cv_emb = await embed_cv(cv)
    jd_emb = await embed_jd(jd)
    score = compute_score(cv_emb, jd_emb)

    import json
    print(json.dumps(score, indent=2))

asyncio.run(test())