import os
import base64
import time
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_SCOPES

class SpotifyAuthManager:
    def __init__(self):
        self.client_id = SPOTIFY_CLIENT_ID
        self.client_secret = SPOTIFY_CLIENT_SECRET
        self.redirect_uri = SPOTIFY_REDIRECT_URI
        self.scopes = SPOTIFY_SCOPES
        self.token_info = None
        self.sp = None
        self.oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scopes,
            cache_path=".spotify_cache"
        )

    def get_auth_url(self):
        return self.oauth.get_authorize_url()

    def handle_callback(self, code):
        self.token_info = self.oauth.get_access_token(code, as_dict=True)
        return self.token_info

    def get_spotify_client(self):
        if not self.token_info:
            raise ValueError("Aucun token — l’utilisateur doit s'authentifier.")
        if self.oauth.is_token_expired(self.token_info):
            self.token_info = self.oauth.refresh_access_token(self.token_info["refresh_token"])
        self.sp = spotipy.Spotify(auth=self.token_info["access_token"])
        return self.sp

class SpotifyDataFetcher:
    def __init__(self, sp):
        self.sp = sp

    def get_top_tracks(self, limit=20):
        try:
            res = self.sp.current_user_top_tracks(limit=limit, time_range="medium_term")
            return res.get("items", [])
        except Exception:
            return []

    def get_top_artists(self, limit=10):
        try:
            res = self.sp.current_user_top_artists(limit=limit, time_range="medium_term")
            return res.get("items", [])
        except Exception:
            return []

    def search_tracks(self, query, limit=10):
        try:
            res = self.sp.search(q=query, type="track", limit=limit)
            return res.get("tracks", {}).get("items", [])
        except Exception:
            return []

class PlaylistManager:
    def __init__(self, sp):
        self.sp = sp

    def create_playlist(self, name, description="Playlist générée via IA"):
        try:
            user_id = self.sp.me()["id"]
            playlist = self.sp.user_playlist_create(user=user_id, name=name, public=False, description=description)
            return playlist
        except Exception as e:
            print("Erreur create_playlist:", e)
            return None

    def add_tracks(self, playlist_id, track_uris):
        try:
            if track_uris:
                self.sp.playlist_add_items(playlist_id, track_uris)
        except Exception as e:
            print("Erreur add_tracks:", e)
