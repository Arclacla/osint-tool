import requests

def geocode_address(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }
    try:
        response = requests.get(url, params=params, headers={"User-Agent": "osint-tool"})
        response.raise_for_status()
        data = response.json()
        if not data:
            return None
        return {
            "lat": float(data[0]["lat"]),
            "lon": float(data[0]["lon"])
        }
    except Exception as e:
        print(f"❌ Erreur géocodage : {e}")
        return None

def build_bbox_from_point(lat, lon, radius_km=5):
    delta = radius_km / 111  # approx. 1° ≈ 111 km
    return [lat - delta, lon - delta, lat + delta, lon + delta]
