import streamlit as st
from spotify_auth import SpotifyAuthManager, SpotifyDataFetcher, PlaylistManager
from ai import GroqRecommender

class PlaylistGenerator:
    def __init__(self):
        self.auth = SpotifyAuthManager()
        self.ai = GroqRecommender()
        self.sp = None
        self.fetcher = None
        self.pm = None

        token_info = st.session_state.get("spotify_token_info")
        if token_info:
            self.auth.token_info = token_info
            self.setup_from_token()

    def setup_from_token(self):
        self.sp = self.auth.get_client()
        if self.sp:
            self.fetcher = SpotifyDataFetcher(self.sp)
            self.pm = PlaylistManager(self.sp)
            return True
        return False

    def start_user_authorization(self):
        auth_url = self.auth.get_auth_url()
        st.info(f"Autorise l'accès Spotify via ce lien : [Clique ici]({auth_url})")
        code = st.text_input("Colle le code d'autorisation Spotify ici :")
        if code.strip():
            token_info = self.auth.exchange_code(code.strip())
            if token_info:
                st.session_state["spotify_token_info"] = self.auth.token_info
                return self.setup_from_token()
        return False

    def get_preferences(self):
        if not self.fetcher:
            return {'tracks': [], 'artists': []}
        return {
            'tracks': self.fetcher.get_top_tracks(),
            'artists': self.fetcher.get_top_artists()
        }

    def generate_playlist(self, prompt=""):
        prefs = self.get_preferences()
        analysis = self.ai.analyze_preferences({"name": "User"}, prefs['tracks'], prefs['artists'])
        recs = self.ai.generate_recommendations(analysis, prompt)

        tracks = []
        if self.fetcher:
            for query in recs.get('queries', []):
                tracks.extend(self.fetcher.search_tracks(query))

        playlist_info = {
            'name': recs.get('name', 'Ma Playlist'),
            'description': analysis.get('vibe', ''),
            'tracks': tracks
        }

        playlist_url = None
        if self.pm and tracks:
            p = self.pm.create_playlist(playlist_info['name'], description=playlist_info['description'])
            if p:
                uris = [t['uri'] for t in tracks]
                self.pm.add_tracks(p['id'], uris)
                playlist_url = p.get('external_urls', {}).get('spotify')

        return playlist_info, playlist_url
