import asyncio
from services.embedder import embed_jd

async def test():
    jd = {
        "required_skills": ["Python", "FastAPI", "PostgreSQL"],
        "preferred_skills": ["Docker", "Redis"],
        "experience_required": "3+ năm kinh nghiệm phát triển backend",
        "education_required": "Cử nhân Khoa học Máy tính hoặc ngành liên quan"
    }
    result = await embed_jd(jd)
    for field, vector in result.items():
        print(f"{field}: {len(vector)} chiều, 3 giá trị đầu: {vector[:3]}")

asyncio.run(test())