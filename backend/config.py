from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
RULES_DIR = BASE_DIR / "rules"
MAX_UPLOAD_BYTES = 15 * 1024 * 1024
APP_VERSION = "0.2.0"
SUPPORTED_SUFFIXES = {".json", ".csv", ".txt", ".log", ".evtx"}
