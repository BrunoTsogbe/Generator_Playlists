import streamlit as st
from playlist_generator import PlaylistGenerator
from config import DEFAULT_PLAYLIST_SIZE, MAX_PLAYLIST_SIZE

st.set_page_config(page_title="🎵 Playlist Generator AI", page_icon="🎵", layout="wide")

if "gen" not in st.session_state:
    st.session_state.gen = PlaylistGenerator()

if "playlist" not in st.session_state:
    st.session_state.playlist = None

if "spotify_token" not in st.session_state:
    st.session_state.spotify_token = None

def main():
    st.title("🎵 Playlist Generator AI")
    st.write("Créez des playlists personnalisées avec l'IA")
    
    with st.sidebar:
        st.header("⚙️ Paramètres")
        theme = st.text_input("🎭 Thème", placeholder="Ex: Étude, Sport, Soirée...")
        size = st.slider("📊 Nombre de tracks", 5, MAX_PLAYLIST_SIZE, DEFAULT_PLAYLIST_SIZE, 5)
        public = st.checkbox("🌐 Public", value=False)

        if st.session_state.spotify_token:
            if st.button("🚪 Logout"):
                st.session_state.spotify_token = None
                st.rerun()
        else:
            st.info("👉 Connectez-vous à Spotify")
            if st.button("🎵 Login"):
                auth_url = st.session_state.gen.auth.get_auth_url()
                st.markdown(f"[Clique ici pour te connecter]({auth_url})")
            code = st.text_input("Colle le code Spotify ici", type="password")
            if code:
                if st.session_state.gen.authenticate(code):
                    st.success("✅ Connecté!")
                    st.rerun()
            return
    
    if st.session_state.gen.setup():
        prefs = st.session_state.gen.get_preferences()
        if prefs:
            if st.button("✨ Générer Playlist"):
                pl = st.session_state.gen.generate(theme, size)
                if pl:
                    st.session_state.playlist = pl
                    st.success("✅ Playlist prête!")
        
        if st.session_state.playlist:
            pl = st.session_state.playlist
            st.subheader(pl['name'])
            st.write(f"**Description:** {pl['description']}")
            st.write("**Tracks:**")
            for i,t in enumerate(pl['tracks'],1):
                st.write(f"{i}. {t['name']} — {t['artist']} ({t['popularity']}%)")
            if st.button("📤 Exporter vers Spotify"):
                st.session_state.gen.export(pl, public)

if __name__ == "__main__":
    main()
