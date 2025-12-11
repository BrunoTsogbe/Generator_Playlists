import streamlit as st
from spotify_auth import SpotifyAuthManager, SpotifyDataFetcher, PlaylistManager
from ai import GroqRecommender

class PlaylistGenerator:
    """Backend : chat IA + création playlist Spotify optionnelle"""

    def __init__(self):
        self.auth = SpotifyAuthManager()
        self.ai = GroqRecommender()
        self.sp = None
        self.fetcher = None
        self.pm = None
        if st.session_state.get("spotify_token"):
            self.setup()

    def setup(self):
        """Initialisation Spotify si token existant"""
        token = st.session_state.get("spotify_token")
        if token:
            self.sp = self.auth.get_client(token)
            if self.sp:
                self.fetcher = SpotifyDataFetcher(self.sp)
                self.pm = PlaylistManager(self.sp)
                return True
        return False

    def authenticate(self, code):
        """Authentifie Spotify via code OAuth"""
        token = self.auth.handle_callback(code)
        if token:
            st.session_state.spotify_token = token
            return self.setup()
        return False

    def get_preferences(self):
        """Récupère top tracks/artists si connecté"""
        if not self.fetcher:
            return {'tracks': [], 'artists': []}
        return {
            'tracks': self.fetcher.get_top_tracks(),
            'artists': self.fetcher.get_top_artists()
        }

    def generate_playlist(self, prompt=""):
        """Génère une playlist complète via l'IA + recherche Spotify si possible"""
        prefs = self.get_preferences()
        analysis = self.ai.analyze_preferences({"name": "User"}, prefs['tracks'], prefs['artists'])
        recs = self.ai.generate_recommendations(analysis, prompt)

        tracks = []
        if self.fetcher:
            for query in recs.get('queries', []):
                results = self.fetcher.search_tracks(query)
                tracks.extend(results)

        playlist_info = {
            'name': recs.get('name', 'Ma Playlist'),
            'description': analysis.get('vibe', ''),
            'tracks': tracks
        }

        playlist_url = None
        if self.pm and tracks:
            # Correction : méthode correcte
            p = self.pm.create_playlist(
                playlist_info['name'],
                description=playlist_info['description'],
                public=False
            )
            if p:
                uris = [t['uri'] for t in tracks]
                self.pm.add_tracks(p['id'], uris)
                # URL Spotify correcte
                playlist_url = p.get('external_urls', {}).get('spotify')

        return playlist_info, playlist_url
