import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from geopy.distance import geodesic

class BusStopNetwork:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = None
        self.graph = nx.Graph()

    def load_data(self):
        self.df = pd.read_csv(self.csv_path)

    def build_nodes(self):
        for _, row in self.df.iterrows():
            self.graph.add_node(
                row['parada_id'],
                name=row['nombre_parada'],
                lat=row['latitud'],
                lon=row['longitud'],
                district=row['localidad'],
                route=row['ruta_alimentador']
            )

    def connect_same_route(self):
        for route in self.df['ruta_alimentador'].unique():
            sub = self.df[self.df['ruta_alimentador'] == route].sort_values('parada_id')
            ids = list(sub['parada_id'])
            for i in range(len(ids) - 1):
                p1 = (sub.iloc[i]['latitud'], sub.iloc[i]['longitud'])
                p2 = (sub.iloc[i + 1]['latitud'], sub.iloc[i + 1]['longitud'])
                dist = geodesic(p1, p2).km
                self.graph.add_edge(ids[i], ids[i + 1], weight=dist)

    def connect_nearby_stops(self, max_distance_km=0.3):
        for i in range(len(self.df)):
            for j in range(i + 1, len(self.df)):
                p1 = (self.df.iloc[i]['latitud'], self.df.iloc[i]['longitud'])
                p2 = (self.df.iloc[j]['latitud'], self.df.iloc[j]['longitud'])
                dist = geodesic(p1, p2).km
                if dist < max_distance_km:
                    self.graph.add_edge(
                        self.df.iloc[i]['parada_id'],
                        self.df.iloc[j]['parada_id'],
                        weight=dist
                    )

    def compute_centrality(self):
        degree_centrality = nx.degree_centrality(self.graph)
        betweenness = nx.betweenness_centrality(self.graph, weight='weight')
        return degree_centrality, betweenness

    def display_top_critical(self, betweenness, top_n=10):
        top_critical = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:top_n]
        print(f"\n🔝 Paradas más importantes por 'betweenness centrality':")
        for stop_id, value in top_critical:
            info = self.graph.nodes[stop_id]
            print(f" - {info['name']} ({info['district']}, {info['route']}): centrality={value:.4f}")

    def visualize(self):
        plt.figure(figsize=(10, 8))
        pos = {n: (self.graph.nodes[n]['lon'], self.graph.nodes[n]['lat']) for n in self.graph.nodes}
        nx.draw(self.graph, pos, node_size=40, node_color='red', edge_color='gray', with_labels=False)
        plt.title("Red de paradas alimentadoras de Bogotá (simulada)")
        plt.xlabel("Longitud")
        plt.ylabel("Latitud")
        plt.show()

    def build_network(self):
        self.load_data()
        self.build_nodes()
        self.connect_same_route()
        self.connect_nearby_stops()
        print(f"Grafo construido con {self.graph.number_of_nodes()} nodos y {self.graph.number_of_edges()} aristas.")


if __name__ == "__main__":
    network = BusStopNetwork("feeder_stops_bogota.csv")
    network.build_network()
    degree_centrality, betweenness = network.compute_centrality()
    network.display_top_critical(betweenness)
    network.visualize()
