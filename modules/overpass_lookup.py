import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

def build_overpass_query(key, value=None, name=None, bbox=None, country=None):
    filters = f'["{key}"="{value}"]' if value else f'["{key}"]'
    if name:
        filters = f'["{key}"="{value}"]' if value else f'["{key}"]'
        if name:
            filters += f'["name"~"{name}",i]'
        if country:
            filters += f'["addr:country"="{country}"]'
    bbox_str = f"({','.join(map(str, bbox))})" if bbox else ""
    query = f"""
    [out:json][timeout:25];
    (
      node{filters}{bbox_str};
      way{filters}{bbox_str};
      relation{filters}{bbox_str};
    );
    out center;
    """
    return query.strip()

def query_overpass(query):
    try:
        response = requests.post(OVERPASS_URL, data={"data": query})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def parse_overpass_results(data):
    if "elements" not in data:
        return []

    results = []
    for el in data["elements"]:
        tags = el.get("tags", {})
        lat = el.get("lat") or el.get("center", {}).get("lat")
        lon = el.get("lon") or el.get("center", {}).get("lon")
        name = tags.get("name", "Sans nom")
        results.append({
            "type": el["type"],
            "name": name,
            "lat": lat,
            "lon": lon,
            "tags": tags
        })
    return results
