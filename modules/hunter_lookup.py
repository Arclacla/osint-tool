import os
import requests
from dotenv import load_dotenv

load_dotenv()

HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")

def hunter_lookup(domain):
    if not HUNTER_API_KEY:
        return {"error": "Aucune clé API Hunter.io configurée dans le fichier .env"}

    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={HUNTER_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": f"Erreur API Hunter.io: HTTP {response.status_code}"}

    data = response.json()
    emails = data.get("data", {}).get("emails", [])
    return [email.get("value") for email in emails]
