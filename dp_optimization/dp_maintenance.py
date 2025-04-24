
from shared.data_loader import load_data
from typing import List, Dict

def allocate_maintenance(budget: float) -> List[Dict]:
    """
    Select roads to maintain using dynamic programming (0/1 Knapsack) based on budget.
    """
    roads_df = load_data("roads")
    roads_df = roads_df.rename(columns={
        "from-id": "from_id",
        "to-id": "to_id",
        "distance-km": "distance",
        "traffic-level": "capacity",
        "condition": "condition"
    })

    valid_roads = []

    for row in roads_df.itertuples(index=False):
        condition = int(row.condition)
        distance = float(row.distance)
        cost = (10 - condition) * 0.1 * distance
        if cost == 0:
            continue

        score = (10 - condition) * row.capacity

        road = {
            "FromID": row.from_id,
            "ToID": row.to_id,
            "Condition": condition,
            "Capacity": row.capacity,
            "Distance": distance,
            "MaintenanceCost": cost,
            "Score": score
        }

        valid_roads.append(road)

    # Knapsack DP
    n = len(valid_roads)
    budget_int = int(budget * 100)  # convert to integer for cents precision
    costs = [int(r["MaintenanceCost"] * 100) for r in valid_roads]
    values = [int(r["Score"]) for r in valid_roads]

    dp = [[0 for _ in range(budget_int + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(budget_int + 1):
            if costs[i-1] <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - costs[i-1]] + values[i-1])
            else:
                dp[i][w] = dp[i-1][w]

    # Backtrack
    selected = []
    w = budget_int
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected.append(i-1)
            w -= costs[i-1]

    return [valid_roads[i] for i in selected]

def print_maintenance_plan(roads: List[Dict]):
    print("\n=== Maintenance Allocation Plan ===")
    for r in roads:
        print(f"{r['FromID']} → {r['ToID']}: Condition {r['Condition']}, Cost = {r['MaintenanceCost']:.2f}M EGP")
    total = sum(r["MaintenanceCost"] for r in roads)
    print(f"\nTotal Cost: {total:.2f}M EGP")

if __name__ == "__main__":
    print("Testing Maintenance Allocation...")
    user_budget = float(input("Enter your maintenance budget (in million EGP): "))
    plan = allocate_maintenance(budget=user_budget)
    print_maintenance_plan(plan)
