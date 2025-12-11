"""Configuration centralisée"""

import os
from dotenv import load_dotenv

# Charge les variables d'environnement depuis .env
load_dotenv()

# ================== SPOTIFY CONFIG ==================
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "https://generator-b.streamlit.app/")

SPOTIFY_SCOPES = [
    "playlist-modify-public",
    "playlist-modify-private",
    "user-read-private",
    "user-top-read",
]

# ================== GROQ CONFIG ==================
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_TEMPERATURE = 0.5
GROQ_MAX_TOKENS = 512

# ================== APP CONFIG ==================
DEFAULT_PLAYLIST_SIZE = 20
MAX_PLAYLIST_SIZE = 50
TRACKS_LIMIT = 20
ARTISTS_LIMIT = 5
SEARCH_LIMIT = 5
CACHE_TTL = 300
