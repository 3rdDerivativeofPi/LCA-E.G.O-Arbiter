import asyncio
from services.llm_client import llm

async def test():
    response = await llm.generate("Hãy chào hỏi bằng một câu ngắn gọn.")
    print(response)

asyncio.run(test())