# E.G.O: Arbiter
### Explainable Governance Optimizer: Arbiter

> An AI agent for HR talent screening — evaluates CVs against job descriptions using semantic matching, explainable scoring, and bias detection.

---

## What It Does

E.G.O: Arbiter helps recruiters screen candidates faster and more fairly. Given a job description and one or more CVs, it:

- **Parses** structured data from CVs and job descriptions using a local LLM
- **Scores** candidates semantically across skills, experience, and education
- **Explains** why a candidate is or isn't a good fit in plain language
- **Detects bias** in job descriptions and suggests fairer alternatives
- **Ranks** multiple candidates against a single job description instantly

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Python 3.12 |
| LLM (text generation) | Ollama + Mistral |
| Embeddings (local) | Ollama + nomic-embed-text |
| Vector search | FAISS |
| Frontend | React + Vite + TypeScript |

Everything runs **fully locally** — no external API calls, no rate limits, no cost.

---

## Project Structure

```
LCA-E.G.O-Arbiter/
├── backend/
│   ├── main.py                  # FastAPI app, CORS, routers
│   ├── config.py                # Environment variables and defaults
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # Local config (not committed)
│   ├── routers/
│   │   ├── evaluate.py          # POST /evaluate/ — single CV evaluation
│   │   └── rank.py              # POST /rank/session — multi-CV ranking
│   └── services/
│       ├── llm_client.py        # Ollama adapter (text + embeddings)
│       ├── parser.py            # CV/JD → structured JSON
│       ├── embedder.py          # Structured JSON → vectors
│       ├── matcher.py           # Weighted cosine similarity scoring
│       ├── explainer.py         # LLM-generated strengths/weaknesses
│       ├── bias_detector.py     # JD bias analysis
│       ├── vector_store.py      # FAISS vector storage and search
│       ├── session_store.py     # In-memory session management
│       └── agent.py             # Full pipeline orchestrator
└── frontend/
    └── src/
        ├── App.tsx              # Tab routing (Evaluate / Rank)
        ├── EvaluateTab.tsx      # Single CV evaluation UI
        ├── RankTab.tsx          # Multi-CV ranking UI
        ├── types.ts             # Shared TypeScript interfaces
        └── index.css            # Global styles (dark gold theme)
```

---

## Pipeline

```
CV (PDF/DOCX/TXT) ──┐
                    ├──► [1] Parser      → structured JSON (LLM)
JD (text) ──────────┘
                         [2] Embedder    → per-field vectors (local)
                         [3] Matcher     → weighted cosine similarity
                         [4] Explainer   → strengths / weaknesses (LLM)
                         [5] Bias Det.   → JD language audit (LLM)
                         [6] Agent Loop  → Observe → Analyze → Decide → Reflect
```

**Scoring weights (default):**
- Skills: 50%
- Experience: 30%
- Education: 20%

---

## Setup

### Prerequisites
- Python 3.12+
- Conda
- Node.js 20+
- [Ollama](https://ollama.com) installed and running

### 1. Pull Ollama models
```bash
ollama pull mistral
ollama pull nomic-embed-text
```

### 2. Backend
```bash
cd backend

# Create and activate conda environment
conda create -n ego-arbiter python=3.12
conda activate ego-arbiter

# Install dependencies
conda install -c conda-forge fastapi uvicorn httpx numpy pydantic python-dotenv
pip install python-multipart pymupdf python-docx faiss-cpu ollama sentence-transformers

# Configure environment
cp .env.example .env
# Edit .env if needed (defaults should work out of the box)

# Start the server
uvicorn main:app --reload
# API available at http://localhost:8000
# Swagger docs at http://localhost:8000/docs
```

### 3. Frontend
```bash
cd frontend
npm install
npm run dev
# UI available at http://localhost:5173
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/evaluate/` | Evaluate single CV against JD |
| POST | `/rank/session` | Create ranking session with JD |
| POST | `/rank/session/{id}/cv` | Upload CV to session |
| GET | `/rank/session/{id}/rank` | Get ranked leaderboard |
| POST | `/rank/session/{id}/explain/{candidate_id}` | Explain a candidate on demand |

Full interactive docs: `http://localhost:8000/docs`

---

## Environment Variables

Create `backend/.env` from the example:

```env
LLM_MODEL=mistral
EMBEDDING_MODEL=nomic-embed-text

WEIGHT_SKILLS=0.50
WEIGHT_EXPERIENCE=0.30
WEIGHT_EDUCATION=0.20
```

---

## Known Limitations

- **Session data is in-memory** — restarting the backend clears all sessions
- **No authentication** — all sessions are currently public
- **PDF parsing** — works best with text-based PDFs; scanned PDFs may not parse well
- **LLM output** — Mistral occasionally produces malformed JSON; the parser retries automatically

---

## Roadmap

- [ ] Persistent database (PostgreSQL or SQLite)
- [ ] User authentication and recruiter accounts
- [ ] Batch CV upload (ZIP file)
- [ ] Improved PDF parsing for scanned documents
- [ ] Landing page and product pitch materials
- [ ] Fine-tuned scoring model for domain-specific roles

---

## Team

**Logic, Compliance & Arbitration (Team LCA)**
- Hoàng Hữu Quang — AI Lead, Backend Architecture