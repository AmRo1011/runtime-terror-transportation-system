
from shared.data_loader import load_data
from typing import Dict, List

def schedule_buses(total_buses: int) -> Dict[str, int]:
    # This part remains as implemented with DP
    routes_df = load_data("bus_routes")
    routes_df = routes_df.rename(columns={"stopscomma-separated-ids": "stops"})

    route_ids: List[str] = []
    scores: List[float] = []
    costs: List[int] = []

    for row in routes_df.itertuples(index=False):
        route_id = row.routeid
        passengers = int(row.dailypassengers)
        stops = row.stops.split(",")
        num_stops = len(stops)
        traffic_weight = 1.2

        score = passengers * num_stops * traffic_weight
        buses_required = max(1, num_stops)

        route_ids.append(route_id)
        scores.append(score)
        costs.append(buses_required)

    n = len(scores)
    W = total_buses
    dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(W + 1):
            if costs[i-1] <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - costs[i-1]] + scores[i-1])
            else:
                dp[i][w] = dp[i-1][w]

    w = W
    selected = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected.append(i-1)
            w -= costs[i-1]

    allocation = {}
    for i in range(n):
        route = route_ids[i]
        if i in selected:
            allocation[route] = costs[i]
        else:
            allocation[route] = 0

    return allocation

def schedule_metro_lines(total_trains: int) -> Dict[str, int]:
    """
    Distribute metro trains across lines using 0/1 Knapsack DP to maximize coverage.
    """
    metro_df = load_data("metro_lines")
    metro_df = metro_df.rename(columns={"daily-passengers": "daily", "stationscomma-separated-ids": "stations"})

    line_ids: List[str] = []
    values: List[float] = []
    costs: List[int] = []

    for row in metro_df.itertuples(index=False):
        line_id = row.lineid
        passengers = int(row.daily)
        stations = row.stations.split(",")
        num_stations = len(stations)
        train_cost = max(1, num_stations)

        line_ids.append(line_id)
        values.append(passengers)  # value is the passenger count
        costs.append(train_cost)

    n = len(values)
    W = total_trains
    dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(W + 1):
            if costs[i-1] <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - costs[i-1]] + values[i-1])
            else:
                dp[i][w] = dp[i-1][w]

    w = W
    selected = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected.append(i-1)
            w -= costs[i-1]

    allocation = {}
    for i in range(n):
        line = line_ids[i]
        if i in selected:
            allocation[line] = costs[i]
        else:
            allocation[line] = 0

    return allocation

def print_schedule(schedule: Dict[str, int], title: str):
    print(f"\n=== {title} ===")
    for route, count in schedule.items():
        print(f"{route}: {count} vehicles")

if __name__ == "__main__":
    print("Testing Transit Scheduling...")
    buses = schedule_buses(60)
    print_schedule(buses, "Bus Schedule")

    metros = schedule_metro_lines(20)
    print_schedule(metros, "Metro Schedule")
