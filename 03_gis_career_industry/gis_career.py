from pathlib import Path
import html

cities = [
    {"city": "Jakarta", "lat": -6.2088, "lon": 106.8456, "jobs": 120, "field": "Data & Software"},
    {"city": "Bandung", "lat": -6.9175, "lon": 107.6191, "jobs": 78, "field": "Software & GIS"},
    {"city": "Yogyakarta", "lat": -7.7956, "lon": 110.3695, "jobs": 55, "field": "Data & Akademik"},
    {"city": "Surabaya", "lat": -7.2575, "lon": 112.7521, "jobs": 68, "field": "Software & Industri"},
    {"city": "Bengkulu", "lat": -3.8004, "lon": 102.2655, "jobs": 18, "field": "GIS & Data"},
]
markers = []
for c in cities:
    popup = html.escape(f"{c['city']} | {c['jobs']} lowongan contoh | {c['field']}")
    markers.append(
        f"L.circleMarker([{c['lat']}, {c['lon']}], "
        f"{{radius:{5 + c['jobs']/12:.1f}, color:'#176B87', fillOpacity:0.65}})"
        f".addTo(map).bindPopup('{popup}');"
    )
page = """<!doctype html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Peta Peluang Karier</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<style>body{font-family:Arial;margin:0;color:#202a35}header{padding:12px 20px}#map{height:78vh}</style>
</head><body><header><h2>Peta Ilustratif Peluang Karier</h2>
<p>Ukuran lingkaran menunjukkan jumlah lowongan ilustratif, bukan data aktual.</p></header>
<div id="map"></div><script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>const map=L.map('map').setView([-2.5,112],5);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
{attribution:'&copy; OpenStreetMap contributors'}).addTo(map);
""" + "\n".join(markers) + "\n</script></body></html>"
Path(__file__).with_name("peta_peluang_karier.html").write_text(page, encoding="utf-8")
print("Peta dibuat: peta_peluang_karier.html")
print("Peluang contoh tertinggi:", max(cities, key=lambda c: c["jobs"])["city"])
