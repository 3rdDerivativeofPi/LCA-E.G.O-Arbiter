from .llm_client import llm

SYSTEM = (
    "Bạn là chuyên gia phân tích nhân sự khách quan. "
    "Viết ngắn gọn, chuyên nghiệp bằng tiếng Việt. "
    "Chỉ trả về JSON hợp lệ, không có markdown hoặc giải thích thêm."
)


async def explain(cv: dict, jd: dict, score: dict) -> dict:
    prompt = f"""
Phân tích ứng viên dưới đây so với mô tả công việc. Hãy ngắn gọn.

ỨNG VIÊN: {cv}
CÔNG VIỆC: {jd}
ĐIỂM SỐ: {score}

Chỉ trả về JSON sau, không có văn bản thêm:
{{
  "strengths": ["tối đa 3 điểm mạnh ngắn gọn"],
  "weaknesses": ["tối đa 3 điểm yếu ngắn gọn"],
  "overall_fit": "một câu tóm tắt mức độ phù hợp",
  "recommendation": "Rất phù hợp | Phù hợp | Cần cân nhắc | Không phù hợp"
}}
"""
    return await llm.generate_json(prompt, SYSTEM)