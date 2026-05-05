import asyncio
import httpx

BASE = "http://localhost:8000"

JD = """
We are looking for a Python Backend Developer with 3+ years of experience.
Required skills: Python, FastAPI, PostgreSQL.
Preferred skills: Docker, Redis, AWS.
Education: Bachelor's degree in Computer Science or related field.
"""

CVS = [
    ("Alice Nguyen", """
    Alice Nguyen. Skills: Python, FastAPI, PostgreSQL, Git, Docker.
    Experience: Backend Developer at Acme (3 years) - Built REST APIs.
    Education: Bachelor's in Computer Science, Hanoi University, 2021.
    """),
    ("Bob Tran", """
    Bob Tran. Skills: Java, Spring Boot, MySQL.
    Experience: Software Engineer at Tech Corp (2 years) - Built microservices.
    Education: Bachelor's in Information Technology, HCM University, 2022.
    """),
    ("Charlie Le", """
    Charlie Le. Skills: Python, Django, PostgreSQL, Redis, AWS.
    Experience: Full Stack Developer at Startup (4 years) - Built web apps.
    Education: Bachelor's in Software Engineering, Da Nang University, 2020.
    """),
]

async def test():
    async with httpx.AsyncClient(timeout=120) as client:
        # 1. Create session
        resp = await client.post(f"{BASE}/rank/session", data={"jd_text": JD})
        session_id = resp.json()["session_id"]
        print(f"Session created: {session_id}")

        # 2. Upload CVs
        for name, cv_text in CVS:
            files = {"cv_file": (f"{name}.txt", cv_text.encode(), "text/plain")}
            resp = await client.post(f"{BASE}/rank/session/{session_id}/cv", files=files)
            print(f"Uploaded: {resp.json()['name']}")

        # 3. Get ranking
        resp = await client.get(f"{BASE}/rank/session/{session_id}/rank")
        leaderboard = resp.json()["leaderboard"]
        print("\nLeaderboard:")
        for c in leaderboard:
            print(f"  #{c['rank']} {c['name']}: {c['score']['total']}%")

asyncio.run(test())