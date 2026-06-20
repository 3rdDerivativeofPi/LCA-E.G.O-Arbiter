import re
from .llm_client import llm

SYSTEM = (
    "Bạn là chuyên viên tuyển dụng (HR) chuyên nghiệp, viết email cho ứng viên "
    "với giọng văn lịch sự, ấm áp và tôn trọng, bằng tiếng Việt. "
    "Trả lời HOÀN TOÀN bằng tiếng Việt. "
    "Chỉ trả về JSON hợp lệ, không có markdown hoặc giải thích thêm."
)

VALID_TYPES = {"invite", "reject"}


def _strip_markdown(text: str) -> str:
    """Remove common markdown artifacts so the email reads as plain text."""
    if not text:
        return text
    # Bold / italic: **text**, __text__, *text*, _text_
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"__(.+?)__", r"\1", text)
    text = re.sub(r"(?<!\w)\*(.+?)\*(?!\w)", r"\1", text)
    text = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"\1", text)
    # Headers: ## Header -> Header
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
    # Bullet markers: - item / * item -> • item (keep list readability)
    text = re.sub(r"^[\-\*]\s+", "• ", text, flags=re.MULTILINE)
    # Stray backticks
    text = text.replace("`", "")
    return text.strip()


def _capitalize_sentences(text: str) -> str:
    """Safety net: capitalize the first letter of each line and after sentence-ending punctuation,
    in case the model produced all-lowercase output."""
    if not text:
        return text

    def cap_match(m: re.Match) -> str:
        return m.group(0).upper()

    # Capitalize start of each line
    text = re.sub(r"(^|\n)\s*([a-zà-ỹ])", lambda m: m.group(1) + m.group(2).upper(), text)
    # Capitalize after . ! ? followed by space
    text = re.sub(r"([.!?]\s+)([a-zà-ỹ])", lambda m: m.group(1) + m.group(2).upper(), text)
    return text


async def generate_email(
    email_type: str,
    cv: dict,
    jd: dict,
    score: dict,
    explanation: dict,
    company_name: str = "",
    sender_name: str = "",
    interview_details: str = "",
) -> dict:
    """
    email_type: "invite" or "reject"
    cv: parsed CV dict (name, skills, experience, education, etc.)
    jd: parsed JD dict (title, etc.)
    score: compute_score() result
    explanation: explain() result (strengths, weaknesses, overall_fit, recommendation)
    interview_details: optional raw notes (time/place/format) for invite emails
    """
    if email_type not in VALID_TYPES:
        raise ValueError(f"email_type must be one of {VALID_TYPES}, got '{email_type}'")

    candidate_name = cv.get("name", "Ứng viên")
    job_title = jd.get("title", "vị trí đang tuyển")

    if email_type == "invite":
        intent_instructions = f"""
Viết email MỜI PHỎNG VẤN cho ứng viên. Email cần:
- Chúc mừng/thông báo ứng viên đã được chọn vào vòng phỏng vấn
- Nhắc đến 1-2 điểm mạnh cụ thể của ứng viên (dựa trên dữ liệu đánh giá) một cách tự nhiên, không lộ liễu là AI chấm điểm
- Đề cập chi tiết phỏng vấn nếu có: {interview_details or "(chưa có chi tiết cụ thể, để placeholder lịch sự như '[Thời gian phỏng vấn]')"}
- Giọng văn tích cực, chuyên nghiệp, chào đón
"""
    else:
        intent_instructions = """
Viết email TỪ CHỐI ứng viên một cách lịch sự và tôn trọng. Email cần:
- Cảm ơn ứng viên đã dành thời gian ứng tuyển
- Thông báo nhẹ nhàng rằng công ty đã chọn ứng viên khác phù hợp hơn ở thời điểm này
- KHÔNG liệt kê điểm yếu cụ thể hay lý do từ chối chi tiết — giữ chung chung, tránh gây tổn thương
- Khuyến khích ứng viên ứng tuyển vào các vị trí khác trong tương lai nếu phù hợp
- Giọng văn ấm áp, tôn trọng, ngắn gọn
"""

    prompt = f"""
QUAN TRỌNG: Viết nội dung email bằng văn bản thuần túy (plain text), viết hoa chữ cái đầu câu
và tên riêng như văn viết bình thường. TUYỆT ĐỐI KHÔNG sử dụng ký hiệu markdown như **, *, _, #
để định dạng. Chỉ dùng dấu câu thông thường và xuống dòng để phân đoạn.

{intent_instructions}

THÔNG TIN:
- Tên ứng viên: {candidate_name}
- Vị trí ứng tuyển: {job_title}
- Công ty: {company_name or "(tên công ty)"}
- Người gửi: {sender_name or "(Bộ phận Tuyển dụng)"}
- Điểm mạnh ứng viên (chỉ dùng cho email mời, KHÔNG dùng cho email từ chối): {explanation.get('strengths', [])}
- Mức độ phù hợp tổng thể: {explanation.get('overall_fit', '')}

Trả về JSON với đúng các khóa sau:
{{
  "subject": "tiêu đề email ngắn gọn, chuyên nghiệp",
  "body": "toàn bộ nội dung email dạng văn bản thuần, có lời chào, nội dung chính, lời kết và chữ ký",
  "type": "{email_type}"
}}
"""
    result = await llm.generate_json(prompt, SYSTEM)

    # Belt-and-suspenders: strip any markdown that slipped through despite instructions,
    # and fix capitalization if the model went all-lowercase
    if "subject" in result:
        result["subject"] = _capitalize_sentences(_strip_markdown(result["subject"]))
    if "body" in result:
        result["body"] = _capitalize_sentences(_strip_markdown(result["body"]))

    # Never trust the LLM to echo this back correctly — we already know it.
    result["type"] = email_type

    return result