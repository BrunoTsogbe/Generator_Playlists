import streamlit as st
from playlist_generator import PlaylistGenerator

st.set_page_config(page_title="Chat IA Playlist", layout="wide")
if "gen" not in st.session_state:
    try:
        st.session_state.gen = PlaylistGenerator()
    except Exception as e:
        st.error(f"Erreur backend : {e}")
        st.stop()

gen = st.session_state.gen

st.sidebar.title("Connexion Spotify")
if not st.session_state.get("spotify_token"):
    if st.sidebar.button("Se connecter à Spotify"):
        auth_url = gen.auth.get_auth_url()
        st.sidebar.markdown(f"[Clique ici pour autoriser Spotify]({auth_url})")
    code = st.sidebar.text_input("Code Spotify (si fourni)")
    if code and gen.authenticate(code):
        st.success("Connecté à Spotify !")
else:
    st.sidebar.success("Spotify connecté ")
st.title("Chat IA Playlist")
user_msg = st.text_area(
    "Parle au bot pour générer ta playlist",
    height=150,
    placeholder="Ex: Crée une playlist chill de 10 tracks afrobeat"
)

if st.button("Envoyer"):
    if user_msg.strip():
        with st.spinner("Le bot réfléchit..."):
            playlist, url = gen.generate_playlist(user_msg)
        st.subheader(f"🎵 {playlist['name']}")
        st.write(f"Description : {playlist.get('description','')}")
        st.write(f"Nombre de tracks : {len(playlist['tracks'])}")
        for i, t in enumerate(playlist['tracks'],1):
            st.write(f"{i}. {t['name']} — {t['artist']}")

        if url:
            st.markdown(f"[Écouter sur Spotify]({url})")
    else:
        st.warning("Écris quelque chose avant d'envoyer.")
