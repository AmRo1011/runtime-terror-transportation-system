from shared.data_loader import load_data
from typing import Dict, List

def schedule_buses(total_buses: int) -> Dict[str, int]:
    """
    Distribute buses across routes using dynamic programming (0/1 Knapsack) to maximize coverage.
    """
    # Load the cleaned bus routes data from the CSV file
    routes_df = load_data("bus_routes")

    # Initialize lists to store route information
    route_ids: List[str] = []
    scores: List[float] = []
    costs: List[int] = []

    # Process each route in the dataset
    for row in routes_df.itertuples(index=False):
        # Get route ID
        route_id = row.routeid
        # Convert daily passengers to integer
        passengers = int(row.dailypassengers)
        # Split stops string into list and count number of stops
        stops = row.stopscomma_separated_ids.split(",")
        num_stops = len(stops)
        # Traffic weight factor to prioritize busy routes
        traffic_weight = 1.2

        # Calculate route score based on passengers, stops, and traffic
        score = passengers * num_stops * traffic_weight
        # Calculate required buses (minimum 1 bus per route)
        buses_required = max(1, num_stops)

        # Store route information
        route_ids.append(route_id)
        scores.append(score)
        costs.append(buses_required)

    # Dynamic Programming (0/1 Knapsack) implementation
    # Get number of routes and total available buses
    n = len(scores)
    W = total_buses
    # Initialize DP table with zeros
    dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]

    # Fill DP table
    for i in range(1, n + 1):
        for w in range(W + 1):
            if costs[i-1] <= w:
                # If we can include current route, choose max of including or excluding
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - costs[i-1]] + scores[i-1])
            else:
                # If we can't include current route, carry forward previous value
                dp[i][w] = dp[i-1][w]

    # Backtrack to find selected routes
    w = W
    selected = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            # If value changed, this route was included
            selected.append(i-1)
            w -= costs[i-1]

    # Create allocation dictionary
    allocation = {}
    for i in range(n):
        route = route_ids[i]
        if i in selected:
            # Assign required buses to selected routes
            allocation[route] = costs[i]
        else:
            # No buses for unselected routes
            allocation[route] = 0

    return allocation

def schedule_metro_lines(total_trains: int) -> Dict[str, int]:
    """
    Distribute metro trains across lines using dynamic programming (0/1 Knapsack) to maximize coverage.
    """
    # Load the cleaned metro lines data from the CSV file
    metro_df = load_data("metro_lines")

    # Initialize lists to store line information
    line_ids: List[str] = []
    values: List[float] = []
    costs: List[int] = []

    # Process each metro line in the dataset
    for row in metro_df.itertuples(index=False):
        # Get line ID
        line_id = row.lineid
        # Convert daily passengers to integer
        passengers = int(row.daily_passengers)
        # Split stations string into list and count number of stations
        stations = row.stationscomma_separated_ids.split(",")
        num_stations = len(stations)
        # Calculate required trains (minimum 1 train per line)
        train_cost = max(1, num_stations)

        # Store line information
        line_ids.append(line_id)
        score = passengers * num_stations
        values.append(score)
        costs.append(train_cost)

    # Dynamic Programming (0/1 Knapsack) implementation
    # Get number of lines and total available trains
    n = len(values)
    W = total_trains
    # Initialize DP table with zeros
    dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]

    # Fill DP table
    for i in range(1, n + 1):
        for w in range(W + 1):
            if costs[i-1] <= w:
                # If we can include current line, choose max of including or excluding
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - costs[i-1]] + values[i-1])
            else:
                # If we can't include current line, carry forward previous value
                dp[i][w] = dp[i-1][w]

    # Backtrack to find selected lines
    w = W
    selected = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            # If value changed, this line was included
            selected.append(i-1)
            w -= costs[i-1]

    # Create allocation dictionary
    allocation = {}
    for i in range(n):
        line = line_ids[i]
        if i in selected:
            # Assign required trains to selected lines
            allocation[line] = costs[i]
        else:
            # No trains for unselected lines
            allocation[line] = 0

    return allocation

def print_schedule(schedule: Dict[str, int], title: str):
    """
    Print the schedule in a readable format.
    """
    print(f"\n=== {title} ===")
    # Print each route/line with its allocated vehicles
    for route, count in schedule.items():
        print(f"{route}: {count} vehicles")

if __name__ == "__main__":
    # Main execution block
    print("Testing Transit Scheduling...")
    # Schedule buses with 60 total buses
    buses = schedule_buses(60)
    print_schedule(buses, "Bus Schedule")

    # Schedule metro lines with 20 total trains
    metros = schedule_metro_lines(20)
    print_schedule(metros, "Metro Schedule")
