import folium

def create_map(results, output_file="results_map.html"):
    if not results:
        print("❌ Aucun résultat à afficher sur la carte.")
        return

    # Centrer la carte sur le premier résultat
    first = results[0]
    m = folium.Map(location=[first['lat'], first['lon']], zoom_start=13)

    for res in results:
        name = res.get('name', 'N/A')
        lat = res['lat']
        lon = res['lon']
        tags = res.get('tags', {})

        popup_text = f"<b>{name}</b><br>Latitude: {lat}<br>Longitude: {lon}<br>Tags: {tags}"
        folium.Marker([lat, lon], popup=popup_text).add_to(m)

    m.save(output_file)
    print(f"✅ Carte générée : {output_file}")
