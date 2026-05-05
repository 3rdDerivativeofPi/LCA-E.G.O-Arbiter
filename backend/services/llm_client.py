import json
import re
import ollama


class LLMClient:
    def __init__(self):
        from config import LLM_MODEL, EMBEDDING_MODEL
        self.model = LLM_MODEL
        self.embed_model = EMBEDDING_MODEL

    async def generate(self, prompt: str, system: str = "") -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = ollama.chat(
            model=self.model,
            messages=messages,
            options={"num_predict": 2048},
        )
        return response["message"]["content"]

    async def generate_json(self, prompt: str, system: str = "") -> dict:
        raw = await self.generate(prompt, system)
        clean = re.sub(r"```json\s*|\s*```", "", raw).strip()
        try:
            decoder = json.JSONDecoder()
            result, _ = decoder.raw_decode(clean)
            return result
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM did not return valid JSON: {e}\nRaw: {raw[:300]}")

    async def embed(self, text: str) -> list[float]:
        response = ollama.embed(
            model=self.embed_model,
            input=text,
        )
        return response.embeddings[0]

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [await self.embed(t) for t in texts]


llm = LLMClient()