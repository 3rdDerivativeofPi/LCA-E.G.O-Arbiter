from .llm_client import llm

SYSTEM = (
    "Bạn là chuyên gia nhân sự (HR) giàu kinh nghiệm, chuyên viết mô tả công việc (JD) "
    "chuyên nghiệp, rõ ràng và hấp dẫn bằng tiếng Việt. "
    "Trả lời HOÀN TOÀN bằng tiếng Việt. "
    "Chỉ trả về JSON hợp lệ, không có markdown hoặc giải thích thêm."
)


async def generate_jd(fields: dict) -> dict:
    """
    fields expected keys (all optional except title):
      title, company, location, work_type,
      required_skills (list[str]), preferred_skills (list[str]),
      experience_required (str), education_required (str),
      responsibilities (str - raw notes from HR),
      perks (str - raw notes from HR)
    """
    prompt = f"""
QUAN TRỌNG: Chỉ trả lời bằng một đối tượng JSON duy nhất. Không viết bất kỳ văn bản giải thích,
lời chào, hoặc bình luận nào trước hoặc sau JSON. Câu trả lời của bạn phải bắt đầu bằng dấu "{{"
và kết thúc bằng dấu "}}".

Dựa trên thông tin do bộ phận nhân sự (HR) cung cấp dưới đây, hãy viết một bản Mô tả Công việc (JD)
đầy đủ, chuyên nghiệp và hấp dẫn bằng tiếng Việt. Mở rộng các ghi chú ngắn gọn của HR thành câu văn
hoàn chỉnh, mạch lạc. Không bịa thêm thông tin không có trong dữ liệu gốc — chỉ diễn đạt lại cho
chuyên nghiệp hơn.

THÔNG TIN TỪ HR:
- Vị trí: {fields.get('title', '')}
- Công ty: {fields.get('company', '')}
- Địa điểm: {fields.get('location', '')}
- Hình thức làm việc: {fields.get('work_type', '')}
- Kỹ năng bắt buộc: {', '.join(fields.get('required_skills', []))}
- Kỹ năng ưu tiên: {', '.join(fields.get('preferred_skills', []))}
- Kinh nghiệm yêu cầu: {fields.get('experience_required', '')}
- Học vấn yêu cầu: {fields.get('education_required', '')}
- Ghi chú trách nhiệm công việc (HR cung cấp thô): {fields.get('responsibilities', '')}
- Ghi chú quyền lợi/phúc lợi (HR cung cấp thô): {fields.get('perks', '')}

Trả về CHÍNH XÁC JSON với đúng các khóa sau, không thêm bất kỳ chữ nào khác ngoài JSON:
{{
  "title": "tên vị trí",
  "full_text": "toàn bộ JD hoàn chỉnh dạng văn bản, có cấu trúc rõ ràng với các phần: Giới thiệu, Trách nhiệm công việc, Yêu cầu, Quyền lợi",
  "required_skills": ["danh sách kỹ năng bắt buộc đã chuẩn hóa"],
  "preferred_skills": ["danh sách kỹ năng ưu tiên đã chuẩn hóa"],
  "experience_required": "string",
  "education_required": "string"
}}

Nhắc lại: chỉ trả lời bằng JSON, bắt đầu bằng "{{" và không có gì khác.
"""
    return await llm.generate_json(prompt, SYSTEM)