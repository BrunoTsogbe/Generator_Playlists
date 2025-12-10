"""Configuration centralisée - Optimisée pour la performance"""

import os
from dotenv import load_dotenv

# Charge les variables d'environnement depuis .env
load_dotenv()

# ================== SPOTIFY CONFIG ==================
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")
SPOTIFY_REDIRECT_URI = os.getenv(
    "SPOTIFY_REDIRECT_URI", "https://generator-b.streamlit.app/"
)

# Scopes Spotify nécessaires pour la lecture et modification des playlists
SPOTIFY_SCOPES = [
    "playlist-modify-public",
    "playlist-modify-private",
    "user-read-private",
    "user-top-read",
]

# ================== GROQ LLM CONFIG ==================
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "mixtral-8x7b-32768"  # Meilleur ratio vitesse/qualité
GROQ_TEMPERATURE = 0.5              # Plus cohérent pour les recommandations
GROQ_MAX_TOKENS = 512                # Limite de tokens pour la vitesse

# ================== APP CONFIG ==================
DEFAULT_PLAYLIST_SIZE = 20
MAX_PLAYLIST_SIZE = 100

# Limites pour récupération rapide des données
TRACKS_LIMIT = 20
ARTISTS_LIMIT = 5
SEARCH_LIMIT = 5

# Cache pour les préférences utilisateur (en secondes)
CACHE_TTL = 300  # 5 minutes
