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
    "You are a structured data extractor. "
    "Return ONLY valid JSON with no extra commentary or markdown fences."
)

CV_SCHEMA = {
    "name": "string",
    "summary": "string",
    "skills": ["list of skill strings"],
    "experience": [{"title": "", "company": "", "duration": "", "description": ""}],
    "education": [{"degree": "", "institution": "", "year": ""}],
}

JD_SCHEMA = {
    "title": "string",
    "summary": "string",
    "required_skills": ["list"],
    "preferred_skills": ["list"],
    "experience_required": "string",
    "education_required": "string",
}


def extract_text(file_bytes: bytes, filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1].lower()
    if ext == "pdf":
        if fitz is None:
            raise RuntimeError("PyMuPDF not installed.")
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        return "\n".join(page.get_text() for page in doc) # type: ignore
    if ext in ("docx", "doc"):
        if docx is None:
            raise RuntimeError("python-docx not installed.")
        doc = docx.Document(io.BytesIO(file_bytes))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    return file_bytes.decode("utf-8", errors="replace")


async def parse_cv(file_bytes: bytes, filename: str) -> dict:
    raw_text = extract_text(file_bytes, filename)
    prompt = (
        f"Extract structured CV data from the text below. "
        f"Return JSON matching exactly this schema: {CV_SCHEMA}\n\n"
        f"CV TEXT:\n{raw_text[:6000]}"
    )
    return await llm.generate_json(prompt, SYSTEM_PROMPT)


async def parse_jd(text: str) -> dict:
    prompt = (
        f"Extract structured job description data from the text below. "
        f"Return JSON matching exactly this schema: {JD_SCHEMA}\n\n"
        f"JD TEXT:\n{text[:4000]}"
    )
    return await llm.generate_json(prompt, SYSTEM_PROMPT)