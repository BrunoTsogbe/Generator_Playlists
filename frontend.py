import streamlit as st
from playlist_generator import PlaylistGenerator

st.set_page_config(page_title="Chat IA Playlist", layout="wide")


if "gen" not in st.session_state:
    st.session_state.gen = PlaylistGenerator()

gen = st.session_state.gen

with st.sidebar:
    st.markdown("Connexion Spotify")

    if not st.session_state.get("spotify_token_info"):
        st.info(
            "Connecte toii."
        )

        if st.button("Se connecter via Spotify"):
            with st.spinner("Ouverture du navigateur… en attente du callback Spotify…"):
                ok = gen.start_user_authorization()
                if ok:
                    st.success("Connexion réussie !")
                else:
                    st.error("La connexion a échoué. Réessaie.")
    else:
        st.success("Spotify est connecté ")

st.title("🎵 Chat IA Playlist")
st.markdown("Discute avec le bot pour générer ta playlist personnalisée.")

# ----------------------
# Container central
# ----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Écris ton message ici…", key="user_input")
    submitted = st.form_submit_button("Envoyer")

if submitted and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})

    if not st.session_state.get("spotify_token_info"):
        st.warning("Connecte-toi à Spotify avant de générer une playlist.")
    else:
        with st.spinner("Le bot réfléchit…"):
            playlist, url = gen.generate_playlist(user_input)

        bot_content = playlist.get("description", "Voici votre playlist générée.")
        st.session_state.messages.append({"role": "bot", "content": bot_content})
        st.session_state.last_playlist = playlist
        st.session_state.last_url = url


for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**Vous :** {msg['content']}")
    else:
        st.markdown(f"**Bot :** {msg['content']}")

if st.session_state.get("last_playlist"):
    playlist = st.session_state.last_playlist
    url = st.session_state.last_url

    st.markdown("---")
    st.subheader(f" Playlist : {playlist['name']}")
    st.markdown(f"**Description :** {playlist.get('description','')}")
    st.markdown(f"**Nombre de morceaux :** {len(playlist['tracks'])}")

    for i, t in enumerate(playlist['tracks'], 1):
        artist = ", ".join([a['name'] for a in t.get('artists', [])])
        st.write(f"{i}. {t.get('name', 'Unknown')} — {artist}")

    if url:
        st.markdown(f"[Écouter sur Spotify]({url})")
