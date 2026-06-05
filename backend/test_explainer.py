import asyncio
from services.explainer import explain

async def test():
    cv = {
        "name": "Nguyễn Thị Lan",
        "skills": ["Python", "FastAPI", "PostgreSQL"],
        "experience": [{"title": "Lập trình viên Backend", "company": "Công ty ABC", "duration": "3 năm", "description": "Xây dựng API RESTful và microservices"}],
        "education": [{"degree": "Cử nhân Khoa học Máy tính", "institution": "Đại học Bách Khoa Hà Nội", "year": "2021"}]
    }
    jd = {
        "title": "Lập trình viên Backend Python",
        "required_skills": ["Python", "FastAPI", "PostgreSQL"],
        "preferred_skills": ["Docker", "Redis"],
        "experience_required": "Hơn 3 năm kinh nghiệm",
        "education_required": "Cử nhân Khoa học Máy tính"
    }
    score = {
        "total": 77.5,
        "breakdown": {"skills": 92.42, "experience": 55.8, "education": 72.75}
    }

    result = await explain(cv, jd, score)
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))

asyncio.run(test())