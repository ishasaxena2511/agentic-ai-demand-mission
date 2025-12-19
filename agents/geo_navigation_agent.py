  import folium
import networkx as nx
from math import radians, cos, sin, asin, sqrt

# ==================================================
# SINGLE SOURCE OF TRUTH (ROUTING SAFE CITIES)
# ==================================================
CITY_COORDS = {
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.6139, 77.2090),
    "Jaipur": (26.9124, 75.7873),
    "Indore": (22.7196, 75.8577),
    "Bengaluru": (12.9716, 77.5946),
}

# ==================================================
# DISTANCE FUNCTION
# ==================================================
def haversine(c1, c2):
    lat1, lon1 = c1
    lat2, lon2 = c2
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 6371 * 2 * asin(sqrt(a))

# ==================================================
# GEO NAVIGATION AGENT
# ==================================================
class GeoNavigationAgent:
    def __init__(self):
        self.graph = nx.Graph()

        for city, coord in CITY_COORDS.items():
            self.graph.add_node(city, coord=coord)

        for c1 in CITY_COORDS:
            for c2 in CITY_COORDS:
                if c1 != c2:
                    self.graph.add_edge(
                        c1, c2,
                        weight=haversine(CITY_COORDS[c1], CITY_COORDS[c2])
                    )

    def plan_multi_stop_route(self, cities, fuel_price):
        for city in cities:
            if city not in CITY_COORDS:
                raise ValueError(f"Routing not supported for: {city}")

        total_distance = 0
        path = []

        for i in range(len(cities) - 1):
            segment = nx.dijkstra_path(
                self.graph, cities[i], cities[i + 1], weight="weight"
            )
            distance = nx.dijkstra_path_length(
                self.graph, cities[i], cities[i + 1], weight="weight"
            )
            total_distance += distance
            path.extend(segment[:-1])

        path.append(cities[-1])

        fuel_cost = round((total_distance / 15) * fuel_price, 2)
        eta = round(total_distance / 60, 2)

        m = folium.Map(location=CITY_COORDS[cities[0]], zoom_start=5)
        for city in path:
            folium.Marker(CITY_COORDS[city], tooltip=city).add_to(m)

        folium.PolyLine([CITY_COORDS[c] for c in path], color="blue").add_to(m)

        return {
            "path": path,
            "distance_km": round(total_distance, 2),
            "eta_hours": eta,
            "fuel_cost": fuel_cost,
            "map": m
        }
