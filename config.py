import os
from dotenv import load_dotenv

load_dotenv()

# Spotify
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8501/")
SPOTIFY_SCOPES = [
    "playlist-modify-public",
    "playlist-modify-private",
    "user-read-private",
    "user-top-read",
]

# Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "mixtral-8x7b-32768"
GROQ_TEMPERATURE = 0.5
GROQ_MAX_TOKENS = 512

# App
DEFAULT_PLAYLIST_SIZE = 20
MAX_PLAYLIST_SIZE = 100
TRACKS_LIMIT = 20
ARTISTS_LIMIT = 5
SEARCH_LIMIT = 5
