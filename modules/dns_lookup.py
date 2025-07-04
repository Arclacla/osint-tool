import dns.resolver

def dns_lookup(domain):
    records = {}
    try:
        records['A'] = [ip.address for ip in dns.resolver.resolve(domain, 'A')]
    except Exception:
        records['A'] = ['-']

    try:
        records['MX'] = [str(mx.exchange) for mx in dns.resolver.resolve(domain, 'MX')]
    except Exception:
        records['MX'] = ['-']

    try:
        records['TXT'] = [txt.to_text().strip('"') for txt in dns.resolver.resolve(domain, 'TXT')]
    except Exception:
        records['TXT'] = ['-']

    return records
