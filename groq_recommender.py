import json
import streamlit as st
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL, GROQ_TEMPERATURE, GROQ_MAX_TOKENS

class GroqRecommender:
    """Moteur de recommandation IA avec Groq"""

    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError("La variable GROQ_API_KEY n'est pas définie !")
        
        # clé passée directement au constructeur
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = GROQ_MODEL

    def _extract_json(self, text):
        """Extrait un JSON même si le modèle renvoie du texte autour"""
        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(text[start:end])
        except:
            pass
        return None

    def analyze_preferences(self, profile, tracks, artists):
        tracks_str = "\n".join([f"- {t['name']} par {t['artist']}" for t in tracks[:5]])
        artists_str = "\n".join([f"- {a['name']} ({', '.join(a['genres'])})" for a in artists[:3]])
        
        prompt = f"""
Analyse rapide du profil musical:

TRACKS:
{tracks_str}

ARTISTS:
{artists_str}

Réponds uniquement en JSON :
{{
  "mood": "ambiance",
  "genres": ["genre1", "genre2"],
  "vibe": "description"
}}
"""
        try:
            msg = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=GROQ_TEMPERATURE,
                max_tokens=GROQ_MAX_TOKENS
            )
            text = msg.choices[0].message.content
            parsed = self._extract_json(text)
            if parsed:
                return parsed
        except Exception as e:
            st.error(f"Erreur analyse IA : {e}")
        
        return {"mood": "Dynamique", "genres": ["Pop","Rock"], "vibe":"Playlist personnalisée"}

    def generate_recommendations(self, analysis, theme=""):
        genres = ", ".join(analysis.get("genres", ["Pop","Rock"])[:2])
        mood = analysis.get("mood","Dynamique")
        
        prompt = f"""
Génère 4-5 requêtes Spotify pour une playlist.

GENRES: {genres}
MOOD: {mood}
{('THEME: ' + theme) if theme else ''}

Réponds uniquement en JSON strict :
{{
  "queries": ["q1","q2","q3"],
  "name": "Nom Playlist"
}}
"""
        try:
            msg = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role":"user","content":prompt}],
                temperature=GROQ_TEMPERATURE,
                max_tokens=256
            )
            text = msg.choices[0].message.content
            parsed = self._extract_json(text)
            if parsed:
                return parsed
        except Exception as e:
            st.error(f"Erreur recommandation IA : {e}")
        
        return {"queries":["Popular music","Great hits","Top tracks"],"name":"My AI Playlist"}
