from modules.dns_lookup import dns_lookup
from modules.whois_lookup import whois_lookup
from modules.hunter_lookup import hunter_lookup
from modules.duckduckgo_dork import duckduckgo_search, build_dork


def ask_list(prompt):
    val = input(prompt).strip()
    return val.split(",") if val else []

def print_section(title, content):
    print(f"\n=== {title} ===")
    if isinstance(content, dict):
        for k, v in content.items():
            print(f"{k}: {v}")
    elif isinstance(content, list):
        for item in content:
            print(f"- {item}")
    else:
        print(content)

if __name__ == "__main__":
    domain = input("🔍 Entrez un nom de domaine : ").strip()

    dns_results = dns_lookup(domain)
    print_section("Résolution DNS", dns_results)

    whois_results = whois_lookup(domain)
    print_section("WHOIS", whois_results)

    hunter_results = hunter_lookup(domain)
    print_section("Emails trouvés via Hunter.io", hunter_results)

    print("\n=== Recherche DuckDuckGo Dork interactive ===")
    domains = ask_list("Domaines (ex: github.com,gitlab.com) ou Enter pour skip : ")
    filetypes = ask_list("Types de fichiers (ex: pdf,docx) ou Enter pour skip : ")
    keywords = ask_list("Mots clés (ex: password,login) ou Enter pour skip : ")

    dorks = build_dork(domains=domains, filetypes=filetypes, keywords=keywords)
    if not dorks:
        print("Aucun dork généré.")
    else:
        for dork in dorks:
            print(f"\n🔎 Dork : {dork}")
            results = duckduckgo_search(dork)
            if not results:
                print("Aucun résultat ou erreur.")
            elif isinstance(results, dict) and "error" in results:
                print(f"Erreur : {results['error']}")
            else:
                for url in results:
                    print(f"- {url}")