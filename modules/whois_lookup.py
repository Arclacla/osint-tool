import whois

def whois_lookup(domain):
    try:
        w = whois.whois(domain)
        return {
            "Registrar": w.registrar,
            "Name Servers": w.name_servers,
            "Creation Date": str(w.creation_date),
            "Expiration Date": str(w.expiration_date),
            "Emails": w.emails
        }
    except Exception as e:
        return {"error": str(e)}
