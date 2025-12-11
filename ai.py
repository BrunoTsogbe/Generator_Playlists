from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL, GROQ_TEMPERATURE, GROQ_MAX_TOKENS

class GroqRecommender:
    """IA pour chat et recommandations playlist"""

    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY manquante")
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = GROQ_MODEL

    def chat(self, message: str) -> str:
        if not message.strip():
            return "Message vide."
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un assistant utile et amical."},
                    {"role": "user", "content": message}
                ],
                temperature=GROQ_TEMPERATURE,
                max_tokens=GROQ_MAX_TOKENS
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            return f"Erreur IA : {e}"

    def analyze_preferences(self, user_info, tracks, artists):
        prompt = f"Analyse les préférences de {user_info['name']}. Top tracks : {tracks}. Top artists : {artists}. Donne 3 thèmes et une description."
        return {"vibe": self.chat(prompt), "queries": ["chill", "pop", "afrobeat"], "name": "Ma Playlist"}

    def generate_recommendations(self, analysis, theme=""):
        queries = [theme] if theme else analysis.get("queries", [])
        name = analysis.get("name", "Playlist IA")
        return {"queries": queries, "name": name}
