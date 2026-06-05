import asyncio
from services.embedder import embed_cv
from services.vector_store import VectorStore

async def test():
    # Use a fresh store (not the singleton) to keep test isolated
    store = VectorStore(dimension=1024)

    candidates = [
        {
            "name": "Nguyễn Thị Lan",
            "skills": ["Python", "FastAPI", "PostgreSQL"],
            "experience": [{"title": "Lập trình viên Backend", "company": "Công ty ABC", "duration": "3 năm", "description": "Xây dựng API RESTful"}],
            "education": [{"degree": "Cử nhân Khoa học Máy tính", "institution": "Đại học Bách Khoa Hà Nội", "year": "2021"}]
        },
        {
            "name": "Trần Văn Bình",
            "skills": ["Java", "Spring Boot", "MySQL"],
            "experience": [{"title": "Kỹ sư phần mềm", "company": "Tập đoàn XYZ", "duration": "2 năm", "description": "Xây dựng microservices"}],
            "education": [{"degree": "Cử nhân Công nghệ Thông tin", "institution": "Đại học Khoa học Tự nhiên TP.HCM", "year": "2022"}]
        },
        {
            "name": "Lê Thị Châu",
            "skills": ["Python", "Django", "MongoDB"],
            "experience": [{"title": "Lập trình viên Full Stack", "company": "Startup DEF", "duration": "1 năm", "description": "Phát triển ứng dụng web"}],
            "education": [{"degree": "Cử nhân Kỹ thuật Phần mềm", "institution": "Đại học Đà Nẵng", "year": "2023"}]
        },
    ]

    for c in candidates:
        emb = await embed_cv(c)
        store.add(emb["skills"], {"name": c["name"]})
        print(f"Đã thêm {c['name']} vào vector store")

    # Search: Python backend profile
    query_cv = {
        "skills": ["Python", "FastAPI", "PostgreSQL"],
        "experience": [],
        "education": []
    }
    query_emb = await embed_cv(query_cv)
    results = store.search(query_emb["skills"], top_k=3)

    print("\nKết quả tìm kiếm:")
    for r in results:
        print(f"  {r['meta']['name']}: {r['score']}%")

asyncio.run(test())