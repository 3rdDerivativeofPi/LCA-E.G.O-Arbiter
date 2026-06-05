from .llm_client import llm

SYSTEM = (
    "Bạn là chuyên gia kiểm toán tuân thủ DEI (Đa dạng, Công bằng và Hòa nhập). "
    "Trả lời ngắn gọn, HOÀN TOÀN bằng tiếng Việt. "
    "Chỉ trả về JSON hợp lệ, không có markdown hoặc giải thích thêm."
)


async def detect_bias(jd_text: str) -> dict:
    prompt = f"""
Phân tích mô tả công việc dưới đây để tìm ngôn ngữ thiên kiến hoặc mang tính loại trừ.
Tìm kiếm: từ ngữ phân biệt giới tính, ngôn ngữ liên quan đến độ tuổi, yêu cầu kinh nghiệm không thực tế,
yêu cầu bằng cấp không cần thiết, thiên kiến văn hóa hoặc địa lý.

MÔ TẢ CÔNG VIỆC:
{jd_text[:3000]}

Trả về JSON với đúng các khóa sau. Tất cả giá trị chuỗi phải bằng tiếng Việt:
{{
  "bias_score": 0-100,
  "flags": [
    {{"phrase": "cụm từ gốc từ JD", "issue": "mô tả vấn đề bằng tiếng Việt", "suggestion": "gợi ý cải thiện bằng tiếng Việt"}}
  ],
  "overall_assessment": "đánh giá tổng thể bằng tiếng Việt",
  "improved_excerpt": "phiên bản viết lại của phần có vấn đề nhất, bằng tiếng Việt"
}}
"""
    return await llm.generate_json(prompt, SYSTEM)