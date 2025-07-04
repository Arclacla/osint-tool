import requests
from bs4 import BeautifulSoup
import time
import urllib.parse

def duckduckgo_search(dork, max_results=10, pause=1):
    """
    Effectue une recherche DuckDuckGo avec le dork donné,
    récupère les URLs des résultats.

    :param dork: chaîne de recherche (ex: '"@domain.com" filetype:pdf')
    :param max_results: nombre max de résultats à récupérer
    :param pause: délai entre les requêtes pour éviter le blocage
    :return: liste d'URLs trouvées
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; OSINT-Tool/1.0; +https://github.com/Arclacla/osint-tool)"
    }
    urls = []
    params = {
        "q": dork,
        "kl": "fr-fr"  # langue FR, modifiable
    }
    url = "https://html.duckduckgo.com/html/"

    try:
        response = requests.post(url, data=params, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("a", {"class": "result__a"}, limit=max_results)
        for a in results:
            href = a.get("href")
            if href:
                urls.append(href)
                if len(urls) >= max_results:
                    break
        time.sleep(pause)
    except Exception as e:
        return {"error": str(e)}

    return urls
