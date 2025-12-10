import streamlit as st
from spotify_auth import SpotifyAuthManager, SpotifyDataFetcher, PlaylistManager
from groq_recommender import GroqRecommender
from config import DEFAULT_PLAYLIST_SIZE

class PlaylistGenerator:
    def __init__(self):
        self.auth = SpotifyAuthManager()
        self.ai = GroqRecommender()
        self.sp = None
        self.fetcher = None
        self.pm = None
    
    def setup(self):
        token = st.session_state.get('spotify_token')
        if token:
            self.sp = self.auth.get_client(token)
            if self.sp:
                self.fetcher = SpotifyDataFetcher(self.sp)
                self.pm = PlaylistManager(self.sp)
                return True
        return False
    
    def authenticate(self, code):
        token = self.auth.handle_callback(code)
        if token:
            st.session_state.spotify_token = token
            return self.setup()
        return False
    
    def get_preferences(self):
        if not self.fetcher:
            return None
        return {
            'tracks': self.fetcher.get_top_tracks(),
            'artists': self.fetcher.get_top_artists()
        }
    
    def generate(self, theme="", size=DEFAULT_PLAYLIST_SIZE):
        if not self.fetcher or not self.pm:
            st.error("Non authentifié")
            return None
        prefs = self.get_preferences()
        if not prefs:
            st.error("Impossible de récupérer vos préférences")
            return None
        st.info("🧠 Analyse en cours...")
        analysis = self.ai.analyze_preferences({"name":"User"}, prefs['tracks'], prefs['artists'])
        st.info("🎵 Génération des requêtes...")
        recs = self.ai.generate_recommendations(analysis, theme)
        st.info("🔍 Recherche des tracks...")
        all_tracks = []
        for query in recs.get('queries',[]):
            tracks = self.fetcher.search_tracks(query)
            all_tracks.extend(tracks)
            if len(all_tracks)>=size:
                break
        all_tracks = all_tracks[:size]
        if not all_tracks:
            st.error("Aucune track trouvée")
            return None
        return {
            'name': recs.get('name','My Playlist'),
            'description': analysis.get('vibe',''),
            'tracks': all_tracks
        }
    
    def export(self, playlist_info, public=False):
        if not self.pm:
            st.error("Non authentifié")
            return False
        p = self.pm.create(playlist_info['name'], playlist_info['description'], public)
        if not p:
            return False
        uris = [t['uri'] for t in playlist_info['tracks']]
        if self.pm.add_tracks(p['id'], uris):
            st.success("✅ Playlist créée!")
            st.markdown(f"[🎵 Play sur Spotify]({p['url']})")
            return True
        return False
