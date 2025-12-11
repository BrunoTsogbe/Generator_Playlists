import os
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "")
SPOTIFY_SCOPES = [
    "user-read-private",
    "user-read-email",
    "playlist-modify-private",
    "playlist-modify-public",
    "user-library-read",
    "user-read-playback-state",
    "user-modify-playback-state",
    "user-top-read"
]
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_TEMPERATURE = 0.5
GROQ_MAX_TOKENS = 512

DEFAULT_PLAYLIST_SIZE = 20
MAX_PLAYLIST_SIZE = 50
TRACKS_LIMIT = 20
ARTISTS_LIMIT = 5
SEARCH_LIMIT = 5
CACHE_TTL = 300  
