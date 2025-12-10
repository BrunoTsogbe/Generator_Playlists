# 🎵 Playlist Generator AI

Génère automatiquement des playlists Spotify personnalisées selon vos goûts grâce à l'IA Groq.

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Créez un fichier `.env` à partir de `.env.example` et renseignez vos clés Spotify et Groq.

## Lancement

```bash
streamlit run frontend.py
```

## Fonctionnalités
- Authentification Spotify (OAuth2)
- Analyse IA des préférences musicales
- Génération rapide de playlists
- Export direct vers votre compte Spotify

## Technologies
- Python, Streamlit, Spotipy, Groq

## Optimisations
- Requêtes API limitées et batchées
- Réponses IA courtes et précises
- Interface minimaliste et rapide

---

**Projet optimisé pour la performance et la simplicité.**
