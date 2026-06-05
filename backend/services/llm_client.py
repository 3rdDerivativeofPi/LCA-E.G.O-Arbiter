import json
import re
import ollama


class LLMClient:
    def __init__(self):
        from config import LLM_MODEL
        self.model = LLM_MODEL

    async def generate(self, prompt: str, system: str = "") -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = ollama.chat(
            model=self.model,
            messages=messages,
            options={"num_predict": 8192},  # was 2048
        )
        return response["message"]["content"]

    async def generate_json(self, prompt: str, system: str = "") -> dict:
        raw = await self.generate(prompt, system)
        # Strip fences — handle leading/trailing whitespace and variation in fence style
        clean = re.sub(r"^\s*```(?:json)?\s*", "", raw.strip())
        clean = re.sub(r"\s*```\s*$", "", clean).strip()
        try:
            decoder = json.JSONDecoder()
            result, _ = decoder.raw_decode(clean)
            return result
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM did not return valid JSON: {e}\nRaw: {raw[:300]}")


llm = LLMClient()