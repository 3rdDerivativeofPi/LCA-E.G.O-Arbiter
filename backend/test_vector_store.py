import asyncio
from services.embedder import embed_cv
from services.vector_store import vector_store

async def test():
    candidates = [
        {
            "name": "Alice",
            "skills": ["Python", "FastAPI", "PostgreSQL"],
            "experience": [{"title": "Backend Developer", "company": "Acme", "duration": "3 years", "description": "Built REST APIs"}],
            "education": [{"degree": "Bachelor's in Computer Science", "institution": "Hanoi University", "year": "2021"}]
        },
        {
            "name": "Bob",
            "skills": ["Java", "Spring Boot", "MySQL"],
            "experience": [{"title": "Software Engineer", "company": "Tech Corp", "duration": "2 years", "description": "Built microservices"}],
            "education": [{"degree": "Bachelor's in Information Technology", "institution": "HCM University", "year": "2022"}]
        },
        {
            "name": "Charlie",
            "skills": ["Python", "Django", "MongoDB"],
            "experience": [{"title": "Full Stack Developer", "company": "Startup", "duration": "1 year", "description": "Built web apps"}],
            "education": [{"degree": "Bachelor's in Software Engineering", "institution": "Da Nang University", "year": "2023"}]
        },
    ]

    # Add all candidates to the vector store
    for c in candidates:
        emb = await embed_cv(c)
        vector_store.add(emb["skills"], {"name": c["name"]})
        print(f"Added {c['name']} to vector store")

    # Search with a query
    query_cv = {
        "skills": ["Python", "FastAPI", "PostgreSQL"],
        "experience": [],
        "education": []
    }
    query_emb = await embed_cv(query_cv)
    results = vector_store.search(query_emb["skills"], top_k=3)

    print("\nTop matches:")
    for r in results:
        print(f"  {r['meta']['name']}: {r['score']}%")

asyncio.run(test())