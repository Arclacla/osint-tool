import os
from modules.dns_lookup import dns_lookup
from modules.whois_lookup import whois_lookup
from modules.hunter_lookup import hunter_lookup
from modules.duckduckgo_dork import duckduckgo_search, build_dork
from modules.exporter import export_results
from modules.overpass_lookup import build_overpass_query, query_overpass, parse_overpass_results

def main_menu():
    print("=== MENU PRINCIPAL ===")
    print("1. Recherche OSINT via nom de domaine")
    print("2. Recherche via DuckDuckGo Dork")
    print("3. Recherche Overpass OpenStreetMap")
    print("0. Quitter")
    return input("Sélectionnez une option : ").strip()

def ask_list(prompt):
    val = input(prompt).strip()
    return val.split(",") if val else []

def prompt_export(data, label="résultat"):
    print(f"\nSouhaitez-vous exporter les {label} ?")
    print("1. Oui, au format JSON")
    print("2. Oui, au format Markdown")
    print("3. Non")
    choice = input("Votre choix : ").strip()
    if choice == "1":
        export_results(data, format="json")
    elif choice == "2":
        export_results(data, format="md")

def run_domain_search():
    domain = input("🔍 Entrez un nom de domaine : ").strip()
    result = {}

    result["dns"] = dns_lookup(domain)
    result["whois"] = whois_lookup(domain)
    result["hunter"] = hunter_lookup(domain)

    print("\n=== Résultats DNS ===")
    print(result["dns"])
    print("\n=== Résultats WHOIS ===")
    print(result["whois"])
    print("\n=== Résultats Hunter.io ===")
    print(result["hunter"])

    prompt_export(result, label="résultats domaine")

def run_dork_search():
    domains = ask_list("Domaines (ex: github.com,gitlab.com) : ")
    filetypes = ask_list("Types de fichiers (ex: pdf,docx) : ")
    keywords = ask_list("Mots clés (ex: password,login) : ")

    all_results = {}
    dorks = build_dork(domains=domains, filetypes=filetypes, keywords=keywords)

    for dork in dorks:
        print(f"\n🔎 Dork : {dork}")
        results = duckduckgo_search(dork)
        if not results or isinstance(results, dict):
            print("❌ Aucun résultat ou erreur.")
        else:
            for url in results:
                print(f"- {url}")
        all_results[dork] = results

    prompt_export(all_results, label="résultats dorks")

def run_overpass_search():
    print("\n=== Recherche Overpass Turbo ===")
    key = input("Tag principal OSM (ex: shop, amenity, man_made...) : ").strip()
    value = input("Valeur de ce tag (ex: bakery, pharmacy...) : ").strip()
    name = input("Nom recherché (Enter pour ignorer) : ").strip() or None

    print("\nZone de recherche :")
    print("1. Toulouse")
    print("2. Marseille")
    print("3. Montpellier")
    print("4. Entrer manuellement (lat1, lon1, lat2, lon2)")
    choix = input("Choisissez une zone : ").strip()

    bbox_presets = {
        "1": [43.56, 1.36, 43.66, 1.50],     # Toulouse
        "2": [43.25, 5.30, 43.35, 5.45],     # Marseille
        "3": [43.59, 3.80, 43.65, 3.95],     # Montpellier
    }

    if choix in bbox_presets:
        bbox = bbox_presets[choix]
    elif choix == "4":
        try:
            print("Format : lat1,lon1,lat2,lon2")
            bbox_input = input("Entrez la bounding box : ").strip()
            bbox = list(map(float, bbox_input.split(",")))
            if len(bbox) != 4:
                raise ValueError
        except:
            print("❌ Bounding box invalide.")
            return
    else:
        print("❌ Choix invalide.")
        return

    query = build_overpass_query(key=key, value=value, name=name, bbox=bbox)
    raw_data = query_overpass(query)

    if "error" in raw_data:
        print(f"Erreur Overpass : {raw_data['error']}")
        return

    results = parse_overpass_results(raw_data)

    if not results:
        print("Aucun résultat trouvé.")
    else:
        print(f"\n✅ {len(results)} résultats trouvés :\n")
        for r in results:
            print(f"- {r['name']} ({r['lat']}, {r['lon']}) | Tags: {r['tags']}")

    prompt_export(results, label="résultats Overpass")

if __name__ == "__main__":
    while True:
        choix = main_menu()
        if choix == "1":
            run_domain_search()
        elif choix == "2":
            run_dork_search()
        elif choix == "3":
            run_overpass_search()
        elif choix == "0":
            print("Au revoir 👋")
            break
        else:
            print("Choix invalide.")
