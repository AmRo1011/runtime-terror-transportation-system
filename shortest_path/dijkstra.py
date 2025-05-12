from shared.data_loader import load_data
import heapq

locations = load_data("neighborhoods")
roads = load_data("roads")

graph = {}
for _, row in roads.iterrows():
    f, t, d = row["from_id"], row["to_id"], row["distance_km"]
    graph.setdefault(f, []).append((t, d))
    graph.setdefault(t, []).append((f, d))

id_to_name = dict(zip(locations["id"], locations["name"]))
name_to_id = {n.lower(): i for i, n in zip(locations["id"], locations["name"])}

def dijkstra(graph, start, end):
    queue = [(0, start, [])]
    visited = set()
    while queue:
        cost, node, path = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)
        path = path + [node]
        if node == end:
            return path, cost
        for neighbor, weight in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(queue, (cost + weight, neighbor, path))
    return [], float("inf")
