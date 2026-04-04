import asyncio
from services.bias_detector import detect_bias

async def test():
    jd = """
    We are looking for a rockstar ninja developer who is young and energetic.
    Must have 10+ years of experience with React (released in 2013).
    He should be able to work in a fast-paced environment.
    Must have a Master's degree in Computer Science.
    Native English speakers preferred.
    """

    result = await detect_bias(jd)
    import json
    print(json.dumps(result, indent=2))

asyncio.run(test())