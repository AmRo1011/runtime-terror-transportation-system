from shared.data_loader import load_data
import heapq
import math

locations = load_data("neighborhoods")
roads = load_data("roads")

graph = {}
coords = {}

for _, row in locations.iterrows():
    coords[row["id"]] = (row["x_coordinate"], row["y_coordinate"])

for _, row in roads.iterrows():
    f, t, d = row["from_id"], row["to_id"], row["distance_km"]
    graph.setdefault(f, []).append((t, d))
    graph.setdefault(t, []).append((f, d))

def haversine(coord1, coord2):
    lon1, lat1 = coord1
    lon2, lat2 = coord2
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def astar(graph, coords, start, goal):
    queue = [(0, 0, start, [])]
    visited = set()
    while queue:
        f, g, node, path = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)
        path = path + [node]
        if node == goal:
            return path, g
        for neighbor, cost in graph.get(node, []):
            if neighbor not in visited:
                h = haversine(coords[neighbor], coords[goal])
                heapq.heappush(queue, (g + cost + h, g + cost, neighbor, path))
    return [], float("inf")
