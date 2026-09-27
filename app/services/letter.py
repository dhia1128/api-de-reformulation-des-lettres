"""Opérations de lecture et de reformulation de lettres."""

import base64

from app.services.ollama import chat


def transcrire_image(image_bytes: bytes, media_type: str) -> str:
    """Transcrit fidèlement l'écriture manuscrite présente dans une image."""
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    prompt = (
        f"Transcris fidèlement et intégralement le texte manuscrit visible sur cette "
        f"image ({media_type}). Ne corrige rien, ne reformule rien, recopie exactement "
        "ce qui est écrit, y compris les fautes éventuelles. Réponds uniquement avec "
        "le texte transcrit, sans commentaire ni introduction."
    )
    return chat(prompt, image_b64)


def formaliser_texte(texte_brut: str) -> str:
    """Reformule une transcription dans un style formel et professionnel."""
    prompt = (
        "Voici une lettre transcrite depuis un manuscrit. Réécris-la dans un style "
        "formel, professionnel et bien structuré (formule d'appel, corps du texte "
        "clair et courtois, formule de politesse finale). Conserve tout le sens, les "
        "faits et les informations d'origine : ne rajoute rien qui ne soit pas dans "
        "le texte source, corrige seulement le ton, la grammaire et la structure.\n\n"
        f"Texte source :\n{texte_brut}\n\n"
        "Réponds uniquement avec la lettre reformulée, sans commentaire."
    )
    return chat(prompt)