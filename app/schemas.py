"""Schémas des données échangées par l'API."""

from pydantic import BaseModel


class TransformResponse(BaseModel):
    lettre_formelle: str


class TranscriptionResponse(BaseModel):
    transcription: str


class FormalisationRequest(BaseModel):
    transcription: str


class FormalisationResponse(BaseModel):
    lettre_formelle: str