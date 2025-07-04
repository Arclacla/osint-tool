import requests
from modules.all_list import *


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


def geocode_departement(departement_name_or_code):
    departement = str(departement_name_or_code).strip()
    # Cas 1 : code de département
    if departement in DEPARTMENTS:
        name = DEPARTMENTS[departement]
        return geocode_query(f"{name}, France")

    # Cas 2 : nom du département
    elif departement.title() in DEPARTMENTS.values():
        # Trouver le code correspondant
        for code, nom in DEPARTMENTS.items():
            if nom.lower() == departement.lower():
                return geocode_query(f"{nom}, France")

    # Sinon
    print("❌ Département inconnu.")
    return None



def geocode_query(query):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "polygon_geojson": 0,
        "addressdetails": 1,
        "limit": 1
    }
    headers = {"User-Agent": "OSINT-Tool/1.0"}

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data and "boundingbox" in data[0]:
            # boundingbox = [lat_min, lat_max, lon_min, lon_max]
            bbox_raw = data[0]["boundingbox"]
            lat_min = float(bbox_raw[0])
            lat_max = float(bbox_raw[1])
            lon_min = float(bbox_raw[2])
            lon_max = float(bbox_raw[3])
            # On retourne au bon format : south, west, north, east
            return [lat_min, lon_min, lat_max, lon_max]

    print("❌ Impossible de géocoder ce département.")
    return None
