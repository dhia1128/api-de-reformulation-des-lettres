"""Configuration de l'application et chemins locaux."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

load_dotenv(BASE_DIR / ".env")

APP_TITLE = "Lettre → Style Formel"
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434").rstrip("/")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5vl:7b")
OLLAMA_NUM_CTX = int(os.environ.get("OLLAMA_NUM_CTX", "8192"))
MAX_FILE_SIZE_MB = 10
ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "image/webp"}