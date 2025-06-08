import osmnx as ox
import networkx as nx
import folium
import numpy as np
from datetime import datetime

# 1. Load Graph 
G = nx.read_graphml("data/jalan_kota_bengkulu.graphml")

# 2. Convert node coordinates and edge lengths to float
for _, data in G.nodes(data=True):
    data['x'] = float(data['x'])
    data['y'] = float(data['y'])

for u, v, k, data in G.edges(keys=True, data=True):
    data['length'] = float(data.get('length', 0))

# 3. Lokasi baru: 
lokasi_awal = (-3.8229, 102.2898)    # Stadion Semarak
lokasi_tujuan = (-3.8280, 102.2935)  # Rumah Dinas Gubernur

# 4. Cari node terdekat 
node_ids = list(G.nodes)
node_coords = np.array([(G.nodes[n]['x'], G.nodes[n]['y']) for n in node_ids])

def get_nearest_node(x, y):
    dists = np.sqrt((node_coords[:, 0] - x)**2 + (node_coords[:, 1] - y)**2)
    return node_ids[np.argmin(dists)]

node_awal = get_nearest_node(lokasi_awal[1], lokasi_awal[0])
node_tujuan = get_nearest_node(lokasi_tujuan[1], lokasi_tujuan[0])

#  5. Rute utama & alternatif (dibalik)
# Rute utama
rute_utama = nx.shortest_path(G, node_awal, node_tujuan, weight='length')

# Tentukan ruas macet (40% tengah dari rute utama)
macet_start = len(rute_utama) // 3
macet_end = 2 * len(rute_utama) // 3
macet_nodes = rute_utama[macet_start:macet_end]

# Salin graf untuk cari jalur alternatif
G_copy = G.copy()

# Hapus edge yang termasuk ruas macet (baik arah u→v maupun v→u)
for i in range(len(macet_nodes) - 1):
    u = macet_nodes[i]
    v = macet_nodes[i + 1]
    if G_copy.has_edge(u, v):
        G_copy.remove_edges_from([(u, v, k) for k in G_copy[u][v].keys()])
    if G_copy.has_edge(v, u):  # Jika graf tidak diarahkan
        G_copy.remove_edges_from([(v, u, k) for k in G_copy[v][u].keys()])

# Cari jalur alternatif dari graf yang telah dikurangi
try:
    rute_alternatif = nx.shortest_path(G_copy, node_awal, node_tujuan, weight='length')
except nx.NetworkXNoPath:
    rute_alternatif = []
    print("⚠ Tidak ditemukan jalur alternatif yang menghindari kemacetan.")


# 6. Hitung jarak
def hitung_jarak(route):
    total = 0.0
    for u, v in zip(route[:-1], route[1:]):
        data = G.get_edge_data(u, v)
        total += float(list(data.values())[0].get('length', 0)) if data else 0
    return int(total)

jarak_utama = hitung_jarak(rute_utama)
jarak_alternatif = hitung_jarak(rute_alternatif)

#7. Simulasi: kemacetan di 40% tengah rute utama
macet_nodes = rute_utama[len(rute_utama)//3 : 2*len(rute_utama)//3]

# 8. Buat peta
m = folium.Map(location=lokasi_awal, zoom_start=15)

# Titik awal & tujuan
folium.Marker(lokasi_awal, tooltip="Stadion Semarak", icon=folium.Icon(color="green")).add_to(m)
folium.Marker(lokasi_tujuan, tooltip="Rumah Dinas Gubernur", icon=folium.Icon(color="red")).add_to(m)

# Rute utama (lancar)
for u, v in zip(rute_utama[:-1], rute_utama[1:]):
    warna = "#FF0000" if u in macet_nodes and v in macet_nodes else "#4285F4"
    folium.PolyLine(
        [(G.nodes[u]['y'], G.nodes[u]['x']), (G.nodes[v]['y'], G.nodes[v]['x'])],
        color=warna,
        weight=6
    ).add_to(m)

# Rute alternatif 
for u, v in zip(rute_alternatif[:-1], rute_alternatif[1:]):
    folium.PolyLine(
        [(G.nodes[u]['y'], G.nodes[u]['x']), (G.nodes[v]['y'], G.nodes[v]['x'])],
        color="#01A43F",
        weight=5,
        dash_array="10,10"
    ).add_to(m)

# Blok kemacetan (merah)
for n in macet_nodes:
    folium.CircleMarker(
        location=(G.nodes[n]['y'], G.nodes[n]['x']),
        radius=4,
        color='red',
        fill=True,
        fill_opacity=0.8,
        popup="Kemacetan Tinggi"
    ).add_to(m)

# Panel info
info_html = f"""
<!-- Panel Informasi Modern -->
<div style="position: fixed; bottom: 20px; left: 20px;
    width: 320px; background: #e3f2fd; padding: 18px;
    border-radius: 14px; box-shadow: 0 2px 15px rgba(0,0,0,0.15);
    z-index: 9999; font-family: 'Segoe UI', sans-serif;
    border-left: 5px solid #2196f3;">
    
    <div style="font-size: 18px; font-weight: bold; color: #0d47a1; margin-bottom: 10px;">
        Rute Lalu Lintas Kota Bengkulu
    </div>

    <div style="font-size: 12px; color: #555; margin-bottom: 15px;">
        {datetime.now().strftime('%H:%M, %d %B %Y')}
    </div>

    <div style="margin-bottom: 10px;">
        <span style="font-weight: bold;">Lokasi Awal:</span><br>
        <span style="color: #0d47a1;">Stadion Semarak</span>
    </div>

    <div style="margin-bottom: 15px;">
        <span style="font-weight: bold;">Lokasi Tujuan:</span><br>
        <span style="color: #0d47a1;">Rumah Dinas Gubernur</span>
    </div>

    <div style="background: white; border: 1px solid #bbdefb; padding: 10px; border-radius: 8px; margin-bottom: 12px;">
        <div style="display: flex; justify-content: space-between;">
            <span>Jarak Utama</span><span style="font-weight: bold;">{jarak_utama:,} m</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span>Jarak Alternatif</span><span style="font-weight: bold;">{jarak_alternatif:,} m</span>
        </div>
    </div>

    <div style="display: flex; justify-content: space-between; font-size: 13px; gap: 6px;">
        <div style="flex: 1; text-align: center; padding: 6px; background: #bbdefb; border-radius: 6px;">
            <b>Jalan Kaki</b><br>{int(jarak_utama/80)} mnt
        </div>
        <div style="flex: 1; text-align: center; padding: 6px; background: #bbdefb; border-radius: 6px;">
            <b>Motor</b><br>{int(jarak_utama/250)} mnt
        </div>
        <div style="flex: 1; text-align: center; padding: 6px; background: #bbdefb; border-radius: 6px;">
            <b>Mobil</b><br>{int(jarak_utama/200)} mnt
        </div>
    </div>
</div>

<!-- Notifikasi Kemacetan -->
<div style="
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 9999;
    background-color: #ffebee;
    color: #c62828;
    padding: 16px 20px;
    border-left: 5px solid #b71c1c;
    border-radius: 12px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    font-size: 14px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    max-width: 280px;">
    
    <strong style="color: #b71c1c;"><i class="fas fa-exclamation-triangle"></i> Kemacetan Terdeteksi</strong>
    <div style="margin-top: 8px;">
        Rute utama mengalami kemacetan.<br>
        Disarankan gunakan <b>rute alternatif</b>.
    </div>
</div>

<!-- Legenda -->
<div style="
    position: fixed;
    top: 20px;
    right: 20px;
    z-index:9999;
    background-color:#fefefe;
    padding:12px;
    border-radius:10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    font-size:13px;
    line-height: 1.5;
    border-left: 4px solid #2196f3;
">
    <strong style="color:#0d47a1;">Legenda:</strong><br>
    <span style="color:#FF0000;">■</span> Jalan Macet<br>
    <span style="color:#4285F4;">■</span> Rute Utama Lancar<br>
    <span style="color:#01A43F;">■</span> Rute Alternatif
</div>
"""
m.get_root().html.add_child(folium.Element(info_html))

# 9. Simpan file
m.save("smartcity_rute_kemacetan.html")
print("✅ File disimpan: smartcity_rute_kemacetan.html")
