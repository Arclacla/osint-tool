import requests
from bs4 import BeautifulSoup
import time

def build_dork(domains=None, filetypes=None, keywords=None):
    dorks = []
    domains = [d.strip() for d in domains] if domains else [None]
    filetypes = [f.strip() for f in filetypes] if filetypes else [None]
    keywords = [k.strip() for k in keywords] if keywords else [None]

    for domain in domains:
        for filetype in filetypes:
            for keyword in keywords:
                parts = []
                if keyword:
                    parts.append(f'"{keyword}"')
                if filetype:
                    parts.append(f'filetype:{filetype}')
                if domain:
                    parts.append(f'site:{domain}')
                dorks.append(" ".join(parts))
    return dorks

def duckduckgo_search(dork, max_results=10, pause=1):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; OSINT-Tool/1.0; +https://github.com/Arclacla/osint-tool)"
    }
    urls = []
    params = {
        "q": dork,
        "kl": "fr-fr"
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
        return urls
    except Exception as e:
        return {"error": str(e)}
