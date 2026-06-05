import io
from .llm_client import llm

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    import docx
except ImportError:
    docx = None

SYSTEM_PROMPT = (
    "Bạn là công cụ trích xuất dữ liệu có cấu trúc. "
    "Chỉ trả về JSON hợp lệ bằng tiếng Việt, không có giải thích hoặc markdown."
)

CV_SCHEMA = {
    "name": "string",
    "summary": "string",
    "skills": ["danh sách kỹ năng"],
    "experience": [{"title": "", "company": "", "duration": "", "description": ""}],
    "education": [{"degree": "", "institution": "", "year": ""}],
}

JD_SCHEMA = {
    "title": "string",
    "summary": "string",
    "required_skills": ["danh sách"],
    "preferred_skills": ["danh sách"],
    "experience_required": "string",
    "education_required": "string",
}


def extract_text(file_bytes: bytes, filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1].lower()
    if ext == "pdf":
        if fitz is None:
            raise RuntimeError("PyMuPDF chưa được cài đặt.")
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        return "\n".join(page.get_text() for page in doc)  # type: ignore
    if ext in ("docx", "doc"):
        if docx is None:
            raise RuntimeError("python-docx chưa được cài đặt.")
        doc = docx.Document(io.BytesIO(file_bytes))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    return file_bytes.decode("utf-8", errors="replace")


async def parse_cv(file_bytes: bytes, filename: str) -> dict:
    raw_text = extract_text(file_bytes, filename)
    prompt = (
        f"Trích xuất dữ liệu CV có cấu trúc từ văn bản dưới đây. "
        f"Trả về JSON khớp chính xác với schema này: {CV_SCHEMA}\n\n"
        f"NỘI DUNG CV:\n{raw_text[:6000]}"
    )
    return await llm.generate_json(prompt, SYSTEM_PROMPT)


async def parse_jd(text: str) -> dict:
    prompt = (
        f"Trích xuất dữ liệu mô tả công việc có cấu trúc từ văn bản dưới đây. "
        f"Trả về JSON khớp chính xác với schema này: {JD_SCHEMA}\n\n"
        f"NỘI DUNG MÔ TẢ CÔNG VIỆC:\n{text[:4000]}"
    )
    return await llm.generate_json(prompt, SYSTEM_PROMPT)