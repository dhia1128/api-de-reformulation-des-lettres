"""Routes des pages web."""

from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.config import STATIC_DIR

router = APIRouter()


@router.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")