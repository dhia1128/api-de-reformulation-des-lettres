# Lettre manuscrite → Lettre formelle

API FastAPI qui prend en photo une lettre écrite au stylo et la retranscrit
dans un style formel et professionnel, en s'appuyant sur un modèle Ollama local
(lecture d'image + reformulation de texte). Aucune clé API n'est nécessaire.

## Installation

```bash
python -m venv venv
source venv/bin/activate       # Windows : venv\Scripts\activate
pip install -r requirements.txt
```

Installez Ollama depuis https://ollama.com/download, puis téléchargez un modèle
compatible avec les images :

```bash
ollama pull qwen2.5vl:7b
```

Par défaut, l'application utilise `qwen2.5vl:7b` sur `http://localhost:11434`.
Vous pouvez personnaliser ces valeurs dans un fichier `.env` à la racine :

```env
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5vl:7b
OLLAMA_NUM_CTX=8192
```

La fenêtre de contexte est réglée à 8192 tokens par défaut pour accepter les
images et les prompts de transcription. Si Ollama utilise trop de mémoire,
réduisez `OLLAMA_NUM_CTX` (par exemple à `6144`).

## Lancement

```bash
uvicorn main:app --reload
```

## Organisation du code

```text
app/
  main.py                 # création de l'application FastAPI
  config.py               # configuration et chemins
  schemas.py              # modèles de requête/réponse
  routers/
    pages.py              # interface web
    letters.py            # endpoints de transcription et de formalisation
  services/
    ollama.py             # communication avec Ollama
    letter.py             # transcription et reformulation
main.py                   # point d'entrée Uvicorn compatible
```

Puis ouvrez http://127.0.0.1:8000 pour tester via l'interface web,
ou appelez directement l'API :

```bash
curl -X POST http://127.0.0.1:8000/api/transcrire \
  -F "file=@ma_lettre.jpg"
```

La route renvoie une transcription. Pour obtenir ensuite la lettre formelle :

```bash
curl -X POST http://127.0.0.1:8000/api/formaliser \
  -H "Content-Type: application/json" \
  -d "{\"transcription\":\"Texte brut de la lettre\"}"
```

## Pistes d'amélioration

- **Streaming** : renvoyer la réponse au fur et à mesure (SSE) plutôt
  qu'en un seul bloc, pour une meilleure expérience utilisateur sur les
  lettres longues.
- **Choix du ton** : ajouter un paramètre `style` (formel administratif,
  formel commercial, formel académique...) pour adapter le prompt de
  reformulation.
- **Export** : générer directement un `.docx` ou `.pdf` de la lettre
  formelle (mise en page avec en-tête, date, formule de politesse).
- **Multi-pages** : accepter plusieurs images (une lettre sur plusieurs
  pages) et les concaténer avant reformulation.
- **Persistance** : stocker l'historique des lettres transformées
  (base de données) si plusieurs utilisateurs utilisent l'app.
- **Authentification** : ajouter une clé API ou un login si l'app est
  exposée publiquement, pour éviter les abus de quota.
