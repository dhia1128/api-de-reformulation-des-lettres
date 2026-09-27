"""Client HTTP minimal pour le serveur Ollama local."""

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.config import OLLAMA_MODEL, OLLAMA_NUM_CTX, OLLAMA_URL


def chat(prompt: str, image_b64: str | None = None) -> str:
    """Envoie un message au modèle configuré et renvoie le texte généré."""
    message: dict[str, Any] = {"role": "user", "content": prompt}
    if image_b64:
        message["images"] = [image_b64]

    request = Request(
        f"{OLLAMA_URL}/api/chat",
        data=json.dumps(
            {
                "model": OLLAMA_MODEL,
                "messages": [message],
                "stream": False,
                "options": {"num_ctx": OLLAMA_NUM_CTX},
            }
        ).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=300) as response:
            result: dict[str, Any] = json.load(response)
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        try:
            detail = json.loads(detail).get("error", detail)
        except json.JSONDecodeError:
            pass
        if exc.code == 404 and "not found" in detail.lower():
            detail = (
                f"Modèle '{OLLAMA_MODEL}' absent. Téléchargez-le avec : "
                f"ollama pull {OLLAMA_MODEL}"
            )
        raise RuntimeError(f"Ollama a répondu HTTP {exc.code} : {detail}") from exc
    except URLError as exc:
        raise RuntimeError(
            "Ollama est inaccessible. Vérifiez qu'il est installé et démarré."
        ) from exc

    content = result.get("message", {}).get("content", "").strip()
    if not content:
        raise RuntimeError("Ollama a renvoyé une réponse vide.")
    return content