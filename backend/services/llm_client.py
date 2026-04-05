import asyncio
import json
import re
import httpx
from config import GEMINI_API_KEY, LLM_MODEL, EMBEDDING_MODEL


class LLMClient:
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.model = LLM_MODEL
        self.embed_model = EMBEDDING_MODEL
        self.base = "https://generativelanguage.googleapis.com/v1beta"

    async def generate(self, prompt: str, system: str = "") -> str:
        await asyncio.sleep(10)  # avoid rate limiting
        url = f"{self.base}/models/{self.model}:generateContent?key={self.api_key}"
        contents = []
        if system:
            contents.append({"role": "user", "parts": [{"text": system}]})
            contents.append({"role": "model", "parts": [{"text": "Understood."}]})
        contents.append({"role": "user", "parts": [{"text": prompt}]})

        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(url, json={"contents": contents})
            resp.raise_for_status()
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]

    async def generate_json(self, prompt: str, system: str = "") -> dict:
        raw = await self.generate(prompt, system)
        clean = re.sub(r"```json\s*|\s*```", "", raw).strip()
        try:
            return json.loads(clean)
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM did not return valid JSON: {e}\nRaw: {raw[:300]}")

    async def embed(self, text: str) -> list[float]:
        url = f"{self.base}/models/{self.embed_model}:embedContent?key={self.api_key}"
        payload = {
            "model": f"models/{self.embed_model}",
            "content": {"parts": [{"text": text}]}
        }
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            return resp.json()["embedding"]["values"]

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [await self.embed(t) for t in texts]


llm = LLMClient()