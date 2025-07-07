import requests
import os 

SAUCENAO_API_URL = "https://saucenao.com/search.php"
SAUCENAO_API_KEY = os.getenv("SAUCENAO_API_KEY")

def search_image_saucenao(image_url):
    params = {
        'output_type': 2,
        'api_key': SAUCENAO_API_KEY,
        'url': image_url,
        'numres': 5
    }
    try:
        resp = requests.get(SAUCENAO_API_URL, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if 'results' in data:
            results = []
            for r in data['results']:
                header = r.get('header', {})
                data_info = r.get('data', {})
                results.append({
                    'similarity': header.get('similarity'),
                    'thumbnail': header.get('thumbnail'),
                    'index_name': header.get('index_name'),
                    'title': data_info.get('title'),
                    'author': data_info.get('member_name') or data_info.get('author_name'),
                    'source': data_info.get('source'),
                    'ext_urls': data_info.get('ext_urls', [])
                })
            return results
        else:
            return []
    except Exception as e:
        print(f"Erreur recherche Saucenao : {e}")
        return []


def run_image_reverse_search():
    image_url = input("Entrez l'URL de l'image à rechercher : ").strip()
    print("Recherche en cours...")
    results = search_image_saucenao(image_url)
    if results:
        print(f"{len(results)} résultats trouvés :")
        for res in results:
            print(f"- Similarité : {res['similarity']}% | Source : {res['source']}")
            print(f"  Titre : {res['title']} | Auteur : {res['author']}")
            print(f"  URL(s) : {', '.join(res['ext_urls'])}")
            print(f"  Miniature : {res['thumbnail']}\n")
    else:
        print("Aucun résultat trouvé.")