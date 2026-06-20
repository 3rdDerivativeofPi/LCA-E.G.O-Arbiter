# E.G.O: Arbiter
### Explainable Governance Optimizer: Arbiter

> An AI agent for HR talent screening — evaluates CVs against job descriptions using semantic matching, explainable scoring, and bias detection. Built for the Vietnamese market.

---

## What It Does

E.G.O: Arbiter helps recruiters screen candidates faster and more fairly. Given a job description and one or more CVs, it:

- **Parses** structured data from CVs and job descriptions using a local LLM
- **Scores** candidates semantically across skills, experience, and education
- **Explains** why a candidate is or isn't a good fit in plain language
- **Detects bias** in job descriptions and suggests fairer alternatives
- **Ranks** multiple candidates against a single job description instantly
- **Generates job descriptions** from structured HR input (title, skills, responsibilities, perks, etc.)
- **Drafts candidate emails** (interview invites and rejections) based on evaluation results, for human review before sending

All processing — parsing, embedding, scoring, explanation, bias detection, JD generation, and email drafting — runs in **Vietnamese**.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Python 3.12 |
| LLM (text generation) | Ollama + Qwen3 (4B, thinking mode disabled) |
| Embeddings (local) | `AITeamVN/Vietnamese_Embedding` via `sentence-transformers` (1024-dim, BGE-M3 based) |
| Vector search | FAISS |
| Frontend | React + Vite + TypeScript |

Everything runs **fully locally** — no external API calls, no rate limits, no cost. The embedding model weights (~1.5GB) download once from Hugging Face on first run, then run entirely offline.

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
│   │   ├── rank.py              # POST /rank/session — multi-CV ranking
│   │   ├── jd.py                # POST /jd/generate — JD generation from HR input
│   │   └── email.py             # POST /email/... — candidate email drafting
│   └── services/
│       ├── llm_client.py        # Ollama adapter (text generation + JSON retry)
│       ├── parser.py            # CV/JD → structured JSON
│       ├── embedder.py          # Structured JSON → vectors (local, Vietnamese_Embedding)
│       ├── matcher.py           # Weighted cosine similarity scoring
│       ├── explainer.py         # LLM-generated strengths/weaknesses
│       ├── bias_detector.py     # JD bias analysis
│       ├── jd_generator.py      # JD generation from structured HR fields
│       ├── email_generator.py   # Interview invite / rejection email drafting
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
                    ├──► [1] Parser      → structured JSON (LLM, Vietnamese)
JD (text) ──────────┘
                         [2] Embedder    → per-field vectors (local, Vietnamese_Embedding)
                         [3] Matcher     → weighted cosine similarity
                         [4] Explainer   → strengths / weaknesses (LLM, Vietnamese)
                         [5] Bias Det.   → JD language audit (LLM, Vietnamese)
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

### 1. Pull the Ollama model
```bash
ollama pull qwen3:4b
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

> **Note:** On first run, `sentence-transformers` will download `AITeamVN/Vietnamese_Embedding` (~1.5GB) from Hugging Face. This happens once and is then cached locally (typically under `~/.cache/huggingface/hub/`). No further downloads or API calls are needed after that.

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
| POST | `/jd/generate` | Generate a full JD from structured HR input |
| POST | `/email/session/{id}/candidate/{candidate_id}` | Draft an interview invite or rejection email for a ranked candidate |

Full interactive docs: `http://localhost:8000/docs`

---

## Environment Variables

Create `backend/.env` from the example:

```env
LLM_MODEL=qwen3:4b

WEIGHT_SKILLS=0.50
WEIGHT_EXPERIENCE=0.30
WEIGHT_EDUCATION=0.20
```

> `EMBEDDING_MODEL` is no longer used — embeddings are handled locally via `sentence-transformers` with a fixed model (`AITeamVN/Vietnamese_Embedding`), not configured through Ollama.

---

## Known Limitations

- **Session data is in-memory** — restarting the backend clears all sessions
- **No authentication** — all sessions are currently public
- **PDF parsing** — works best with text-based PDFs; scanned PDFs may not parse well
- **LLM output** — Qwen3 occasionally produces malformed or off-schema JSON; `llm_client.py` retries once with a corrective re-prompt before raising
- **Email and JD generation are human-in-the-loop by design** — outputs are drafts for review, never sent or published automatically

---

## Roadmap

- [ ] Persistent database (PostgreSQL or SQLite)
- [ ] User authentication and recruiter accounts
- [ ] Batch CV upload (ZIP file)
- [ ] Improved PDF parsing for scanned documents
- [ ] Landing page and product pitch materials
- [ ] Fine-tuned scoring model for domain-specific roles
- [ ] Frontend support for JD generation and email drafting flows

---

## Team

**Logic, Compliance & Arbitration (Team LCA)**
- Hoàng Hữu Quang — AI Lead, Backend Architecture