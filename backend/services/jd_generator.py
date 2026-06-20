from .llm_client import llm

SYSTEM = (
    "Bạn là chuyên gia tuyển dụng (HR) và copywriter giàu kinh nghiệm, chuyên viết mô tả công việc (JD) "
    "chuyên nghiệp, hấp dẫn và thuyết phục bằng tiếng Việt. Bạn không chỉ diễn đạt lại ghi chú của HR — "
    "bạn còn bổ sung giá trị: viết đoạn giới thiệu hấp dẫn, làm nổi bật điểm thu hút của vị trí, "
    "và tổ chức nội dung theo cấu trúc chuyên nghiệp mà một JD thực tế trên thị trường sẽ có. "
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
    required_skills = fields.get("required_skills", [])
    preferred_skills = fields.get("preferred_skills", [])

    prompt = f"""
QUAN TRỌNG: Chỉ trả lời bằng một đối tượng JSON duy nhất, đúng với schema bên dưới.
Không viết bất kỳ văn bản giải thích, lời chào, hoặc bình luận nào trước hoặc sau JSON.
Câu trả lời của bạn phải bắt đầu bằng dấu "{{" và kết thúc bằng dấu "}}".
TUYỆT ĐỐI KHÔNG được bỏ sót bất kỳ khóa nào trong schema, kể cả khi giá trị là danh sách rỗng.

NHIỆM VỤ: Viết một bản Mô tả Công việc (JD) đầy đủ, chuyên nghiệp và HẤP DẪN bằng tiếng Việt, dựa trên
thông tin do HR cung cấp dưới đây. Đây không phải là việc chép lại nguyên văn ghi chú của HR — hãy:
1. Viết một đoạn GIỚI THIỆU thu hút về công ty và lý do vị trí này đáng để ứng tuyển (có thể suy luận
   hợp lý từ tên công ty/ngành nghề, nhưng không bịa số liệu cụ thể như doanh thu, số nhân viên).
2. Diễn giải các ghi chú trách nhiệm công việc thành các gạch đầu dòng rõ ràng, chuyên nghiệp.
3. Trong phần "Yêu cầu", PHẢI trình bày ĐẦY ĐỦ CẢ HAI mục riêng biệt: "Kỹ năng bắt buộc" VÀ
   "Kỹ năng ưu tiên" (nếu có kỹ năng ưu tiên trong dữ liệu HR cung cấp). Đây là lỗi nghiêm trọng
   nếu bỏ sót kỹ năng ưu tiên — không được gộp chung hoặc bỏ qua.
4. Trình bày quyền lợi một cách hấp dẫn, không chỉ liệt kê khô khan.
Không bịa thêm THÔNG TIN CỤ THỂ (số liệu, tên công nghệ, mức lương) không có trong dữ liệu gốc —
chỉ được sáng tạo về CÁCH DIỄN ĐẠT và CẤU TRÚC.

THÔNG TIN TỪ HR:
- Vị trí: {fields.get('title', '')}
- Công ty: {fields.get('company', '')}
- Địa điểm: {fields.get('location', '')}
- Hình thức làm việc: {fields.get('work_type', '')}
- Kỹ năng bắt buộc: {', '.join(required_skills) if required_skills else '(không có)'}
- Kỹ năng ưu tiên: {', '.join(preferred_skills) if preferred_skills else '(không có)'}
- Kinh nghiệm yêu cầu: {fields.get('experience_required', '')}
- Học vấn yêu cầu: {fields.get('education_required', '')}
- Ghi chú trách nhiệm công việc (HR cung cấp thô): {fields.get('responsibilities', '')}
- Ghi chú quyền lợi/phúc lợi (HR cung cấp thô): {fields.get('perks', '')}

Trả về CHÍNH XÁC JSON với đúng các khóa sau, không thêm bất kỳ chữ nào khác ngoài JSON.
Nếu danh sách kỹ năng ưu tiên rỗng trong dữ liệu gốc, trả về mảng rỗng [], KHÔNG được bỏ khóa này:
{{
  "title": "tên vị trí",
  "full_text": "toàn bộ JD hoàn chỉnh dạng văn bản, có cấu trúc rõ ràng với các phần: Giới thiệu, Trách nhiệm công việc, Yêu cầu, Quyền lợi",
  "required_skills": {required_skills if required_skills else []},
  "preferred_skills": {preferred_skills if preferred_skills else []},
  "experience_required": "string",
  "education_required": "string"
}}

Nhắc lại: chỉ trả lời bằng JSON, bắt đầu bằng "{{", bao gồm ĐẦY ĐỦ 6 khóa ở trên, không có gì khác.
"""
    result = await llm.generate_json(prompt, SYSTEM)

    # Server-side schema normalization — never let a malformed/partial LLM
    # response leak missing keys to the frontend. Fall back to the HR's
    # original input for skills since those are factual, not generative.
    normalized = {
        "title": result.get("title") or fields.get("title", ""),
        "full_text": result.get("full_text") or "",
        "required_skills": result.get("required_skills") if isinstance(result.get("required_skills"), list) else required_skills,
        "preferred_skills": result.get("preferred_skills") if isinstance(result.get("preferred_skills"), list) else preferred_skills,
        "experience_required": result.get("experience_required") or fields.get("experience_required", ""),
        "education_required": result.get("education_required") or fields.get("education_required", ""),
    }

    # Safety net: if preferred skills exist but the LLM's prose never mentioned
    # even one of them, the model likely dropped that section. Append it rather
    # than silently ship an incomplete JD.
    pref_skills = normalized["preferred_skills"]
    if pref_skills and normalized["full_text"]:
        mentioned = any(skill.lower() in normalized["full_text"].lower() for skill in pref_skills)
        if not mentioned:
            normalized["full_text"] += (
                "\n\nKỹ năng ưu tiên (cộng điểm): " + ", ".join(pref_skills) + "."
            )

    return normalized