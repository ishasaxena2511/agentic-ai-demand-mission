from agents.geo_navigation_agent import GeoNavigationAgent

agent = GeoNavigationAgent()

cities = [
    "Mumbai",
    "Pune",
    "Indore",
    "Jaipur",
    "Delhi"
]

result = agent.plan_multi_stop_route(
    cities=cities,
    fuel_price=105
)

print("Route:", result["path"])
print("Total Distance (km):", result["distance_km"])
print("ETA (hours):", result["eta_hours"])
print("Fuel Cost (₹):", result["fuel_cost"])

result["map"].save("multi_stop_route.html")
