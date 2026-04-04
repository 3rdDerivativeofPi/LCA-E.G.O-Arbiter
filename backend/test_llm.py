import asyncio
from services.llm_client import llm

async def test():
    response = await llm.generate("Say hello in one sentence.")
    print(response)

asyncio.run(test())