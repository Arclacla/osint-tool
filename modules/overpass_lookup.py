import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

def build_overpass_query(key, value=None, name=None, bbox=None, country=None):
    # Construction des filtres tags
    filters = f'["{key}"="{value}"]' if value else f'["{key}"]'
    
    # Ajouter filtre sur le nom (pas sur "value" car potentiellement None)
    if name:
        filters += f'["name"~"{name}",i]'
    # Filtre pays
    if country:
        filters += f'["addr:country"="{country}"]'

    bbox_str = ""
    if bbox and len(bbox) == 4:
        # bbox attendue: [lat_min, lon_min, lat_max, lon_max]
        lat_min, lon_min, lat_max, lon_max = bbox
        # On vérifie l'ordre (au cas où)
        south = min(lat_min, lat_max)
        north = max(lat_min, lat_max)
        west = min(lon_min, lon_max)
        east = max(lon_min, lon_max)

        # **Ordonner dans l’ordre attendu par Overpass: (south, west, north, east)**
        bbox_str = f"({south},{west},{north},{east})"

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
