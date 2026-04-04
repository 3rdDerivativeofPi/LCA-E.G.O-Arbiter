import asyncio
from services.explainer import explain

async def test():
    cv = {
        "name": "Alice",
        "skills": ["Python", "FastAPI", "PostgreSQL"],
        "experience": [{"title": "Backend Developer", "company": "Acme", "duration": "3 years", "description": "Built REST APIs"}],
        "education": [{"degree": "Bachelor's in Computer Science", "institution": "Hanoi University", "year": "2021"}]
    }
    jd = {
        "title": "Python Backend Developer",
        "required_skills": ["Python", "FastAPI", "PostgreSQL"],
        "preferred_skills": ["Docker", "Redis"],
        "experience_required": "3+ years",
        "education_required": "Bachelor's in Computer Science"
    }
    score = {
        "total": 77.5,
        "breakdown": {"skills": 92.42, "experience": 55.8, "education": 72.75}
    }

    result = await explain(cv, jd, score)
    import json
    print(json.dumps(result, indent=2))

asyncio.run(test())