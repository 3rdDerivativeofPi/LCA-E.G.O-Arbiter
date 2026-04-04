import asyncio
from services.parser import parse_jd

async def test():
    jd = """
    We are looking for a Python Backend Developer with 3+ years of experience.
    Required skills: Python, FastAPI, PostgreSQL.
    Preferred skills: Docker, Redis, AWS.
    Education: Bachelor's degree in Computer Science or related field.
    """
    result = await parse_jd(jd)
    import json
    print(json.dumps(result, indent=2))

asyncio.run(test())