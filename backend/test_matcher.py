import asyncio
from services.embedder import embed_cv, embed_jd
from services.matcher import compute_score

async def test():
    cv = {
        "skills": ["Python", "FastAPI", "PostgreSQL"],
        "experience": [{"title": "Lập trình viên Backend", "company": "Công ty ABC", "duration": "3 năm", "description": "Xây dựng các API RESTful và microservices"}],
        "education": [{"degree": "Cử nhân Khoa học Máy tính", "institution": "Đại học Bách Khoa Hà Nội", "year": "2021"}]
    }
    jd = {
        "required_skills": ["Python", "FastAPI", "PostgreSQL"],
        "preferred_skills": ["Docker", "Redis"],
        "experience_required": "Hơn 3 năm kinh nghiệm phát triển backend",
        "education_required": "Cử nhân Khoa học Máy tính hoặc ngành liên quan"
    }

    cv_emb = await embed_cv(cv)
    jd_emb = await embed_jd(jd)
    score = compute_score(cv_emb, jd_emb)

    import json
    print(json.dumps(score, indent=2, ensure_ascii=False))

asyncio.run(test())