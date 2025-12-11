import streamlit as st
from playlist_generator import PlaylistGenerator

# ----------------------
# Config page
# ----------------------
st.set_page_config(page_title="Chat IA Playlist", layout="wide")

# ----------------------
# Backend
# ----------------------
if "gen" not in st.session_state:
    try:
        st.session_state.gen = PlaylistGenerator()
    except Exception as e:
        st.error(f"Erreur backend : {e}")
        st.stop()

gen = st.session_state.gen

# ----------------------
# Sidebar Spotify
# ----------------------
with st.sidebar:
    st.markdown("## Connexion Spotify")
    st.markdown("Connecte-toi pour créer des playlists personnalisées avec tes top tracks.")
    if not st.session_state.get("spotify_token"):
        if st.button("Se connecter à Spotify"):
            auth_url = gen.auth.get_auth_url()
            st.markdown(f"[Autoriser Spotify]({auth_url})")
    else:
        st.success("Spotify connecté")

# ----------------------
# Section principale
# ----------------------
st.title("Chat IA Playlist")
st.markdown("Discute avec le bot pour générer ta playlist personnalisée")

# ----------------------
# Container central
# ----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Formulaire pour envoyer un message
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Écris ton message ici…", key="user_input")
    submitted = st.form_submit_button("Envoyer")

# ----------------------
# Traitement du message
# ----------------------
if submitted and user_input.strip():
    st.session_state.messages.append({"role":"user","content":user_input})
    with st.spinner("Le bot réfléchit…"):
        playlist, url = gen.generate_playlist(user_input)

    bot_content = playlist.get("description","Voici votre playlist générée.")
    st.session_state.messages.append({"role":"bot","content":bot_content})
    st.session_state.last_playlist = playlist
    st.session_state.last_url = url

# ----------------------
# Affichage messages
# ----------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**Vous :** {msg['content']}")
    else:
        st.markdown(f"**Bot :** {msg['content']}")

# ----------------------
# Affichage playlist si générée
# ----------------------
if st.session_state.get("last_playlist"):
    playlist = st.session_state.last_playlist
    url = st.session_state.last_url

    st.markdown("---")
    st.subheader(f"Playlist : {playlist['name']}")
    st.markdown(f"Description : {playlist.get('description','')}")
    st.markdown(f"Nombre de tracks : {len(playlist['tracks'])}")

    for i, t in enumerate(playlist['tracks'], 1):
        artist = t.get('artist', t.get('artists',[{'name':'Unknown'}])[0]['name'])
        track_name = t.get('name','Unknown')
        st.write(f"{i}. {track_name} — {artist}")

    if url:
        st.markdown(f"[Écouter sur Spotify]({url})")
