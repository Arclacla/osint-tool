import os
from modules.dns_lookup import dns_lookup
from modules.whois_lookup import whois_lookup
from modules.hunter_lookup import hunter_lookup
from modules.duckduckgo_dork import duckduckgo_search, build_dork
from modules.exporter import export_results

def main_menu():
    print("=== MENU PRINCIPAL ===")
    print("1. Recherche OSINT via nom de domaine")
    print("2. Recherche via DuckDuckGo Dork")
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

if __name__ == "__main__":
    while True:
        choix = main_menu()
        if choix == "1":
            run_domain_search()
        elif choix == "2":
            run_dork_search()
        elif choix == "0":
            print("Au revoir 👋")
            break
        else:
            print("Choix invalide.")
