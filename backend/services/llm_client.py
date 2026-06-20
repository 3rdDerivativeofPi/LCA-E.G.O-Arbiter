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
        messages.append({"role": "user", "content": prompt + "\n/no_think"})

        response = ollama.chat(
            model=self.model,
            messages=messages,
            options={"num_predict": 8192},
        )
        return response["message"]["content"]

    def _clean_json_text(self, raw: str) -> str:
        # Strip any leftover thinking block
        clean = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL)
        # Strip code fences
        clean = re.sub(r"^\s*```(?:json)?\s*", "", clean.strip())
        clean = re.sub(r"\s*```\s*$", "", clean).strip()
        return clean

    async def generate_json(self, prompt: str, system: str = "", _retry: bool = True) -> dict:
        raw = await self.generate(prompt, system)
        clean = self._clean_json_text(raw)
        try:
            decoder = json.JSONDecoder()
            result, _ = decoder.raw_decode(clean)
            return result
        except json.JSONDecodeError as e:
            if _retry:
                # The model answered conversationally instead of with JSON.
                # Re-prompt it once, showing it what it did wrong.
                correction_prompt = f"""
Yêu cầu trước đó của bạn KHÔNG được trả lời đúng định dạng. Bạn đã trả lời bằng văn bản thường
thay vì JSON. Dưới đây là câu trả lời sai của bạn:

---
{raw[:500]}
---

Hãy trả lời LẠI yêu cầu sau đây, lần này CHỈ bằng một đối tượng JSON hợp lệ,
không có bất kỳ văn bản nào khác:

{prompt}
"""
                return await self.generate_json(correction_prompt, system, _retry=False)
            raise ValueError(f"LLM did not return valid JSON: {e}\nRaw: {raw[:300]}")


llm = LLMClient()