import os
from modules.dns_lookup import dns_lookup
from modules.whois_lookup import whois_lookup
from modules.hunter_lookup import hunter_lookup
from modules.duckduckgo_dork import duckduckgo_search, build_dork
from modules.overpass_lookup import build_overpass_query, query_overpass, parse_overpass_results
from modules.geocode import geocode_address, build_bbox_from_point, geocode_departement
from modules.map_visualization import create_map
from datas.all_list import *
from modules.WMN_search import run_username_search
from modules.utils import *
from modules.saucenao_search import search_image_saucenao, run_image_reverse_search


def main_menu():
    print("=== MENU PRINCIPAL ===")
    print("1. Recherche OSINT via nom de domaine")
    print("2. Recherche via DuckDuckGo Dork")
    print("3. Recherche Overpass OpenStreetMap")
    print("4. Recherche de nom d'utilisateur (WhatsMyName)")
    print("5. Recherche d'image inversée (SauceNao)")
    print("0. Quitter")
    return input("Sélectionnez une option : ").strip()



def ask_list(prompt):
    val = input(prompt).strip()
    return val.split(",") if val else []


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



def input_with_help_loop(prompt: str, options: list = None, allow_skip=True) -> str | None:
    """
    Invite l'utilisateur à saisir une valeur.
    Si 'help' est tapé, affiche la liste des options (une fois),
    Puis redemande.
    Si allow_skip est True, l'utilisateur peut taper 'skip' pour passer (retourne None).
    Reboucle tant que la saisie n'est pas dans options (si options données).
    """
    shown_help = False
    while True:
        val = input(prompt).strip()
        val_lower = val.lower()

        if val_lower == "help":
            if options:
                print("\nListe des options possibles :")
                for opt in options:
                    print(f"- {opt}")
                print()
                shown_help = True
            else:
                print("Aucune option disponible à afficher.")
        elif allow_skip and val_lower == "skip":
            return None
        else:
            # Si on a une liste d'options, vérifie que val est dedans
            if options:
                # Autorise saisie non sensible à la casse
                options_lower = [o.lower() for o in options]
                if val_lower in options_lower:
                    # Retourne la forme originale (sensible à casse)
                    idx = options_lower.index(val_lower)
                    return options[idx]
                else:
                    print(f"\n⚠️ '{val}' n'est pas dans la liste des options valides. Tape 'help' pour afficher la liste, ou 'skip' pour ignorer. ")
            else:
                # Pas de liste d'options, retourne direct
                return val



def run_overpass_search():
    print("\n=== Recherche Overpass Turbo ===")

    keys = list(OSM_TAGS.keys())
    key = input_with_help_loop(
        "Tag principal OSM. Tapez 'help' : ",
        options=keys,
        allow_skip=False  # ici on veut un tag obligatoire
    )
    if not key:
        print("Tag principal obligatoire, arrêt. ")
        return

    values = OSM_TAGS.get(key, [])
    if values:
        value = input_with_help_loop(
            f"Valeur pour '{key}'. Tapez 'help' pour la liste, 'skip' pour ignorer : ",
            options=values,
            allow_skip=True
        )
    else:
        value = input(f"Entrez une valeur pour '{key}' : ").strip()

    name = input("Nom recherché (Enter pour ignorer) : ").strip() or None
    print("\nMode de zone géographique :")
    print("1. Zone prédéfinie (Toulouse, Marseille, etc.)")
    print("2. Autour d'une adresse (via géocodage)")
    print("3. Bounding box manuelle")
    print("4. Recherche par pays (utilise tag addr:country)")
    print("5. Recherche par départements (nom ou code)")
    zone_mode = input("Choisissez un mode : ").strip()

    bbox = None
    country_filter = None

    if zone_mode == "1":
        print("1. Toulouse\n2. Marseille\n3. Montpellier")
        choix = input("Choisissez une ville : ").strip()
        bbox_presets = {
            "1": [43.56, 1.36, 43.66, 1.50],
            "2": [43.25, 5.30, 43.35, 5.45],
            "3": [43.59, 3.80, 43.65, 3.95],
        }
        bbox = bbox_presets.get(choix)

    elif zone_mode == "2":
        adresse = input("Entrez une adresse ou ville : ").strip()
        radius = input("Rayon en km (par défaut 5) : ").strip()
        radius = float(radius) if radius else 5.0
        coords = geocode_address(adresse)
        if not coords:
            print("❌ Adresse introuvable.")
            return
        bbox = build_bbox_from_point(coords["lat"], coords["lon"], radius)

    elif zone_mode == "3":
        try:
            bbox_input = input("lat1,lon1,lat2,lon2 : ").strip()
            bbox = list(map(float, bbox_input.split(",")))
            if len(bbox) != 4:
                raise ValueError
        except:
            print("❌ Bounding box invalide.")
            return

    elif zone_mode == "4":
        country = input("Code pays ISO (ex: FR, BE, MA...) : ").strip().upper()
        country_filter = country

    elif zone_mode == "5":
        print("\n--- Liste des départements ---")
        # Affiche les départements triés par code
        for code, name_dep in sorted(DEPARTMENTS.items()):
            print(f"{code} : {name_dep}")
        
        choix_dep = input("\nEntrez le code ou le nom du département (ou 'exit' pour annuler) : ").strip()
        if choix_dep.lower() == "exit":
            print("Recherche département annulée.")
            return

        # Recherche code à partir du nom (insensible à la casse)
        code_dep = None
        if choix_dep.upper() in DEPARTMENTS:
            code_dep = choix_dep.upper()
        else:
            # Cherche par nom (insensible casse)
            for code, nom in DEPARTMENTS.items():
                if nom.lower() == choix_dep.lower():
                    code_dep = code
                    break

        if not code_dep:
            print("❌ Département non trouvé.")
            return

        print(f"Département sélectionné : {code_dep} - {DEPARTMENTS[code_dep]}")

        # Appel fonction géocodage pour récupérer la bbox
        bbox = geocode_departement(code_dep)
        if not bbox:
            print("❌ Impossible de géocoder ce département.")
            return

    else:
        print("❌ Choix invalide.")
        return

    # Construction et exécution requête
    query = build_overpass_query(
        key=key,
        value=value,
        name=name,
        bbox=bbox,
        country=country_filter
    )

    raw_data = query_overpass(query)

    if "error" in raw_data:
        print(f"Erreur Overpass : {raw_data['error']}")
        return

    results = parse_overpass_results(raw_data)

    if not results:
        print("\nAucun résultat trouvé.")
    else:
        print(f"\n✅ {len(results)} résultats trouvés :\n")
        for r in results:
            print(f"- {r['name']} ({r['lat']}, {r['lon']}) | Tags: {r['tags']}")

    prompt_export(results, label="résultats Overpass")

    create_map_choice = input("Voulez-vous générer une carte interactive des résultats ? (o/N) : ").strip().lower()
    if create_map_choice == "o":
        create_map(results)

if __name__ == "__main__":
    while True:
        choix = main_menu()
        if choix == "1":
            run_domain_search()
        elif choix == "2":
            run_dork_search()
        elif choix == "3":
            run_overpass_search()
        elif choix == "4":
            run_username_search(prompt_export)
        elif choix == "5":
            run_image_reverse_search()
        elif choix == "0":
            print("Au revoir 👋")
            break
        else:
            print("Choix invalide.")
