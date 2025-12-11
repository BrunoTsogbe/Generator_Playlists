import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_SCOPES, TRACKS_LIMIT, ARTISTS_LIMIT, SEARCH_LIMIT

class SpotifyAuthManager:
    def __init__(self):
        self.sp_oauth = SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=",".join(SPOTIFY_SCOPES),
            cache_path=".spotify_cache"
        )

    def get_auth_url(self):
        return self.sp_oauth.get_authorize_url()

    def handle_callback(self, code):
        try:
            return self.sp_oauth.get_access_token(code)
        except Exception as e:
            st.error(f"Erreur d'authentification: {e}")
            return None

    def get_client(self, token_info):
        if not token_info:
            return None
        try:
            if self._is_expired(token_info):
                token_info = self._refresh(token_info)
            if token_info:
                return spotipy.Spotify(auth=token_info['access_token'])
        except Exception as e:
            st.error(f"Erreur client Spotify: {e}")
        return None

    def _is_expired(self, token):
        import time
        return token.get('expires_at', 0) - time.time() < 60

    def _refresh(self, token):
        try:
            return self.sp_oauth.refresh_access_token(token.get('refresh_token', ''))
        except Exception as e:
            st.error(f"Erreur refresh Spotify: {e}")
            return None

class SpotifyDataFetcher:
    def __init__(self, sp):
        self.sp = sp

    def get_user_profile(self):
        try:
            user = self.sp.current_user()
            return {
                'name': user.get('display_name', 'User'),
                'url': user.get('external_urls', {}).get('spotify', ''),
                'followers': user.get('followers', {}).get('total', 0)
            }
        except:
            return {'name':'User','url':'','followers':0}

    def get_top_tracks(self, limit=TRACKS_LIMIT):
        try:
            results = self.sp.current_user_top_tracks(limit=limit)
            return [{'name': t['name'], 'artist': ', '.join(a['name'] for a in t['artists']), 'uri': t['uri']} for t in results.get('items',[])]
        except:
            return []

    def get_top_artists(self, limit=ARTISTS_LIMIT):
        try:
            results = self.sp.current_user_top_artists(limit=limit)
            return [{'name': a['name'], 'genres': a.get('genres',[])[:3]} for a in results.get('items',[])]
        except:
            return []

    def search_tracks(self, query, limit=SEARCH_LIMIT):
        try:
            results = self.sp.search(q=query, type='track', limit=limit)
            return [{'name': t['name'], 'artist': ', '.join(a['name'] for a in t['artists']), 'uri': t['uri']} for t in results.get('tracks',{}).get('items',[])]
        except:
            return []

class PlaylistManager:
    def __init__(self, sp):
        self.sp = sp

    def create(self, name, description="", public=False):
        try:
            user_id = self.sp.current_user()['id']
            p = self.sp.user_playlist_create(user_id, name, public=public, description=description[:300])
            return {'id': p['id'], 'name': p['name'], 'url': p.get('external_urls', {}).get('spotify','')}
        except Exception as e:
            st.error(f"Erreur création playlist: {e}")
            return None

    def add_tracks(self, playlist_id, track_uris):
        try:
            for i in range(0, len(track_uris), 100):
                self.sp.playlist_add_items(playlist_id, track_uris[i:i+100])
            return True
        except Exception as e:
            st.error(f"Erreur ajout tracks: {e}")
            return False
