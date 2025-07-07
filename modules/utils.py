import json
from datetime import datetime

def export_results(data, format="json"):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"export_{now}.{format}"

    try:
        if format == "json":
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        elif format == "md":
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"# Export OSINT - {now}\n\n")
                for key, value in data.items():
                    f.write(f"## {key}\n")
                    if isinstance(value, dict):
                        for subkey, subval in value.items():
                            f.write(f"- **{subkey}**: {subval}\n")
                    elif isinstance(value, list):
                        for item in value:
                            f.write(f"- {item}\n")
                    else:
                        f.write(f"{value}\n")
                    f.write("\n")
        print(f"✅ Résultats exportés dans : {filename}")
    except Exception as e:
        print(f"❌ Erreur d'export : {e}")


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