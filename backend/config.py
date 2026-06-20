import os
from dotenv import load_dotenv

load_dotenv()

# Ollama models (local, no API key needed)
LLM_MODEL = os.getenv("LLM_MODEL", "qwen3:4b")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

# Keep Gemini key optional in case we need fallback
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Default scoring weights (must sum to 1.0)
DEFAULT_WEIGHTS = {
    "skills":     0.50,
    "experience": 0.30,
    "education":  0.20,
}