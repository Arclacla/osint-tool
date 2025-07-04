from modules.dns_lookup import dns_lookup
from modules.whois_lookup import whois_lookup
from modules.hunter_lookup import hunter_lookup
from modules.duckduckgo_dork import duckduckgo_search


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

    print("\n=== Résultats DuckDuckGo Dork ===")
    dork = input("🔍 Tape un dork DuckDuckGo à tester : ").strip()
    if dork:
        ddg_results = duckduckgo_search(dork)
        if isinstance(ddg_results, dict) and "error" in ddg_results:
            print(f"Erreur DuckDuckGo : {ddg_results['error']}")
        elif len(ddg_results) == 0:
            print("Aucun résultat trouvé.")
        else:
            for url in ddg_results:
                print(f"- {url}")
