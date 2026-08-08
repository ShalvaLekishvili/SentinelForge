from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.services.analyzer import analyze_bytes

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="SentinelForge API",
    version="0.1.0",
    description="SOC investigation and detection engineering workbench.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def dashboard():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "SentinelForge", "version": "0.1.0"}


@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="A filename is required.")
    suffix = Path(file.filename).suffix.lower()
    if suffix not in {".json", ".csv", ".txt", ".log"}:
        raise HTTPException(status_code=415, detail="Supported formats: JSON, CSV, TXT, LOG")
    data = await file.read()
    if len(data) > 5 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File exceeds the 5 MB MVP limit.")
    return analyze_bytes(data, suffix=suffix, source_name=file.filename)
