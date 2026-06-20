from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import evaluate, rank, jd, email

app = FastAPI(title="E.G.O: Arbiter API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(evaluate.router, prefix="/evaluate", tags=["evaluate"])
app.include_router(rank.router, prefix="/rank", tags=["rank"])
app.include_router(jd.router, prefix="/jd", tags=["jd"])
app.include_router(email.router, prefix="/email", tags=["email"])

@app.get("/health")
async def health():
    return {"status": "ok", "service": "E.G.O: Arbiter"}