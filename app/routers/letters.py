"""Routes API pour la transformation des lettres."""

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import ALLOWED_CONTENT_TYPES, MAX_FILE_SIZE_MB
from app.schemas import (
    FormalisationRequest,
    FormalisationResponse,
    TranscriptionResponse,
)
from app.services.letter import formaliser_texte, transcrire_image

router = APIRouter(prefix="/api", tags=["lettres"])


@router.post("/transcrire", response_model=TranscriptionResponse)
async def transcrire_lettre(file: UploadFile = File(...)) -> TranscriptionResponse:
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Format non supporté : {file.content_type}. Utilisez PNG, JPEG ou WebP.",
        )

    image_bytes = await file.read()
    if len(image_bytes) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail=f"Fichier trop volumineux (max {MAX_FILE_SIZE_MB} Mo).",
        )

    try:
        transcription = transcrire_image(image_bytes, file.content_type)
        if not transcription:
            raise HTTPException(
                status_code=422,
                detail="Aucun texte n'a pu être lu sur cette image.",
            )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Erreur API : {exc}") from exc

    return TranscriptionResponse(transcription=transcription)


@router.post("/formaliser", response_model=FormalisationResponse)
def formaliser_lettre(
    payload: FormalisationRequest,
) -> FormalisationResponse:
    if not payload.transcription.strip():
        raise HTTPException(status_code=422, detail="La transcription est vide.")

    try:
        lettre_formelle = formaliser_texte(payload.transcription)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Erreur API : {exc}") from exc

    return FormalisationResponse(lettre_formelle=lettre_formelle)