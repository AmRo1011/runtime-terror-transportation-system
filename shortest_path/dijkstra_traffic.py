from shared.data_loader import load_data
import heapq

roads = load_data("roads")
traffic = load_data("traffic")

graph = {}
for _, row in roads.iterrows():
    f, t, d = row["from_id"], row["to_id"], row["distance_km"]
    graph.setdefault(f, []).append((t, d))
    graph.setdefault(t, []).append((f, d))

traffic_data = {}
for _, row in traffic.iterrows():
    key = row["roadid"]
    traffic_data[key] = {
        "morning": row["morning_peakveh/h"],
        "afternoon": row["afternoonveh/h"],
        "evening": row["evening_peakveh/h"],
        "night": row["nightveh/h"]
    }

def calculate_cost(n1, n2, base, traffic_data, period):
    key1 = f"{n1}-{n2}"
    key2 = f"{n2}-{n1}"
    info = traffic_data.get(key1) or traffic_data.get(key2)
    if not info:
        return base
    level = info.get(period, 1000)
    return base * (1 + level / 10000)

def dijkstra_with_traffic(graph, traffic_data, start, end, period):
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
        for neighbor, base in graph.get(node, []):
            if neighbor not in visited:
                adj = calculate_cost(node, neighbor, base, traffic_data, period)
                heapq.heappush(queue, (cost + adj, neighbor, path))
    return [], float("inf")
