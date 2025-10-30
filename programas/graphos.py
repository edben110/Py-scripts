import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from geopy.distance import geodesic

# Load dataset
df = pd.read_csv("feeder_stops_bogota.csv")

# Create graph
G = nx.Graph()

# Add nodes (bus stops)
for _, row in df.iterrows():
    G.add_node(
        row['parada_id'],
        name=row['nombre_parada'],
        lat=row['latitud'],
        lon=row['longitud'],
        district=row['localidad'],
        route=row['ruta_alimentador']
    )

# Connect stops within the same feeder route (simulate sequential order)
for route in df['ruta_alimentador'].unique():
    sub = df[df['ruta_alimentador'] == route].sort_values('parada_id')
    ids = list(sub['parada_id'])
    for i in range(len(ids) - 1):
        # Compute geographic distance (in km)
        p1 = (sub.iloc[i]['latitud'], sub.iloc[i]['longitud'])
        p2 = (sub.iloc[i + 1]['latitud'], sub.iloc[i + 1]['longitud'])
        dist = geodesic(p1, p2).km
        G.add_edge(ids[i], ids[i + 1], weight=dist)

# Connect nearby stops (< 0.3 km)
for i in range(len(df)):
    for j in range(i + 1, len(df)):
        p1 = (df.iloc[i]['latitud'], df.iloc[i]['longitud'])
        p2 = (df.iloc[j]['latitud'], df.iloc[j]['longitud'])
        dist = geodesic(p1, p2).km
        if dist < 0.3:
            G.add_edge(df.iloc[i]['parada_id'], df.iloc[j]['parada_id'], weight=dist)

print(f"Graph built with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")

# Compute centrality metrics
degree_centrality = nx.degree_centrality(G)
betweenness = nx.betweenness_centrality(G, weight='weight')

# Display the 10 most critical stops
top_critical = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:10]
print("\n🔝 Most important stops by 'betweenness centrality':")
for stop_id, value in top_critical:
    info = G.nodes[stop_id]
    print(f" - {info['name']} ({info['district']}, {info['route']}): centrality={value:.4f}")

# Basic graph visualization (non-geographical)
plt.figure(figsize=(10, 8))
pos = {n: (G.nodes[n]['lon'], G.nodes[n]['lat']) for n in G.nodes}
nx.draw(G, pos, node_size=40, node_color='red', edge_color='gray', with_labels=False)
plt.title("Feeder bus stop network in Bogotá (simulated)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
