from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.config import APP_VERSION, FRONTEND_DIR, MAX_UPLOAD_BYTES, SUPPORTED_SUFFIXES
from backend.services.analyzer import analyze_bytes
from backend.services.rule_engine import load_rules

app = FastAPI(
    title="SentinelForge API",
    version=APP_VERSION,
    description="Defensive SOC investigation, telemetry normalization and detection engineering workbench.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response


@app.get("/")
def dashboard():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "SentinelForge", "version": APP_VERSION, "rules": len(load_rules())}


@app.get("/api/rules")
def rules():
    return [{
        "id": rule["id"],
        "title": rule["title"],
        "severity": rule["severity"],
        "confidence": rule.get("confidence", "medium"),
        "mitre": rule.get("mitre", []),
        "source": rule.get("_source", ""),
    } for rule in load_rules()]


@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="A filename is required.")
    suffix = Path(file.filename).suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        raise HTTPException(status_code=415, detail=f"Supported formats: {', '.join(sorted(SUPPORTED_SUFFIXES))}")
    data = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="File exceeds the 15 MB limit.")
    try:
        return analyze_bytes(data, suffix=suffix, source_name=file.filename)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.exception_handler(Exception)
async def unhandled_exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"detail": "Internal analysis error", "type": exc.__class__.__name__})
