from modules.dns_lookup import dns_lookup
from modules.whois_lookup import whois_lookup
from modules.hunter_lookup import hunter_lookup

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
