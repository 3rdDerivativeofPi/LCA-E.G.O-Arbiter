import asyncio
from services.agent import run_pipeline

async def test():
    jd = """
    We are looking for a Python Backend Developer with 3+ years of experience.
    Required skills: Python, FastAPI, PostgreSQL.
    Preferred skills: Docker, Redis, AWS.
    Education: Bachelor's degree in Computer Science or related field.
    """

    cv_text = """
    Alice Nguyen
    Backend Developer with 3 years of experience.
    Skills: Python, FastAPI, PostgreSQL, Git
    Experience: Backend Developer at Acme (3 years) - Built REST APIs and microservices.
    Education: Bachelor's in Computer Science, Hanoi University, 2021.
    """

    result = await run_pipeline(cv_text.encode(), "alice.txt", jd)

    print(f"Candidate: {result['candidate']}")
    print(f"Total Score: {result['score']['total']}%")
    print(f"Breakdown: {result['score']['breakdown']}")
    print(f"Recommendation: {result['explanation']['recommendation']}")
    print(f"Bias Score: {result['bias_report']['bias_score']}")
    print(f"Agent Flags: {result['agent_flags']}")

asyncio.run(test())