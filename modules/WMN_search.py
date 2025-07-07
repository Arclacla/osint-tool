import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

DATAPATH = os.path.join("datas", "wmn-data.json")
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

def load_whatsmyname_db(path=DATAPATH):
    if not os.path.isfile(path):
        print(f"❌ Fichier JSON introuvable : {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Le JSON a une clé "sites" contenant la liste des sites
    return data.get("sites", [])

def check_site(site, username):
    url = site["uri_check"].replace("{account}", username)
    try:
        resp = requests.get(url, timeout=7)
        # Vérifie le code de réponse attendu
        if resp.status_code == site.get("e_code", 200):
            # Si on a une string à rechercher dans la page pour valider la présence
            e_str = site.get("e_string")
            m_str = site.get("m_string")
            m_code = site.get("m_code")

            # Si on a une string à exclure (page d'erreur) ou un code erreur
            if m_str and m_str in resp.text:
                return None
            if m_code and resp.status_code == m_code:
                return None

            if e_str:
                if e_str in resp.text:
                    return {"site": site["name"], "url": url}
                else:
                    return None
            else:
                # Pas de e_string, on considère que status code suffit
                return {"site": site["name"], "url": url}
    except requests.RequestException:
        return None
    return None

def search_username_parallel(username, sites):
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(check_site, site, username) for site in sites]
        for future in tqdm(as_completed(futures), total=len(sites), desc="Recherche en cours"):
            res = future.result()
            if res:
                results.append(res)
    return results

def run_username_search(prompt_export_callback=None):
    print("\n=== Recherche de nom d'utilisateur (WhatsMyName) ===")
    username = input("Entrez le nom d'utilisateur à rechercher : ").strip()
    if not username:
        print("❌ Nom d'utilisateur vide, annulation.")
        return

    print("Chargement de la base de données...")
    sites = load_whatsmyname_db()
    if not sites:
        print("❌ Impossible de charger la base de données.")
        return

    print("Recherche en cours, cela peut prendre un moment...\n")
    results = search_username_parallel(username, sites)

    if not results:
        print(f"\n🔍 0 résultats trouvés pour '{username}' :(")
    else:
        print(f"\n🔍 {len(results)} résultats trouvés pour '{username}' :")
        for i, res in enumerate(results, 1):
            print(f"{i}. {res['site']} : {res['url']}")

    if prompt_export_callback:
        prompt_export_callback(results, f"whatsmyname_{username}")

if __name__ == "__main__":
    # simple test en standalone
    run_username_search()
