from shared.data_loader import load_data
from typing import List, Dict

def allocate_maintenance(budget: float) -> List[Dict]:
    """
    Select roads to maintain using dynamic programming (0/1 Knapsack) based on budget.
    """
    # Load the cleaned roads data from the CSV file
    roads_df = load_data("roads")

    # Initialize a list to store valid roads that need maintenance
    valid_roads = []

    # Process each road in the dataset
    for row in roads_df.itertuples(index=False):
        # Convert road condition to integer (1-10 scale)
        condition = int(row.condition)
        # Convert distance to float (in kilometers)
        distance = float(row.distance_km)
        # Calculate maintenance cost: worse condition and longer distance = higher cost
        cost = (10 - condition) * 0.1 * distance
        # Skip roads that don't need maintenance (cost = 0)
        if cost == 0:
            continue

        # Calculate road importance score: worse condition and higher traffic = higher priority
        score = (10 - condition) * row.traffic_level

        # Create a dictionary with all road information
        road = {
            "FromID": row.from_id,        # Starting point ID
            "ToID": row.to_id,            # Ending point ID
            "Condition": condition,        # Current road condition (1-10)
            "Capacity": row.traffic_level, # Traffic level (vehicles per day)
            "Distance": distance,          # Road length in kilometers
            "MaintenanceCost": cost,       # Estimated maintenance cost
            "Score": score                 # Priority score for maintenance
        }

        # Add this road to the list of valid roads
        valid_roads.append(road)

    # Dynamic Programming (0/1 Knapsack) implementation
    # Get number of roads and convert budget to integer (for cents precision)
    n = len(valid_roads)
    budget_int = int(budget * 100)  # convert to integer for cents precision
    
    # Extract costs and values for DP
    costs = [int(r["MaintenanceCost"] * 100) for r in valid_roads]
    values = [int(r["Score"]) for r in valid_roads]

    # Initialize DP table with zeros
    dp = [[0 for _ in range(budget_int + 1)] for _ in range(n + 1)]

    # Fill DP table
    for i in range(1, n + 1):
        for w in range(budget_int + 1):
            if costs[i-1] <= w:
                # If we can include current road, choose max of including or excluding
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - costs[i-1]] + values[i-1])
            else:
                # If we can't include current road, carry forward previous value
                dp[i][w] = dp[i-1][w]

    # Backtrack to find selected roads
    selected = []
    w = budget_int
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            # If value changed, this road was included
            selected.append(i-1)
            w -= costs[i-1]

    # Return list of selected roads for maintenance
    return [valid_roads[i] for i in selected]

def print_maintenance_plan(roads: List[Dict]):
    """
    Print the maintenance plan in a readable format.
    """
    print("\n=== Maintenance Allocation Plan ===")
    # Print each selected road with its details
    for r in roads:
        print(f"{r['FromID']} → {r['ToID']}: Condition {r['Condition']}, Cost = {r['MaintenanceCost']:.2f}M EGP")
    # Calculate and print total cost
    total = sum(r["MaintenanceCost"] for r in roads)
    print(f"\nTotal Cost: {total:.2f}M EGP")

if __name__ == "__main__":
    # Main execution block
    print("Testing Maintenance Allocation...")
    # Get budget from user
    user_budget = float(input("Enter your maintenance budget (in million EGP): "))
    # Generate maintenance plan
    plan = allocate_maintenance(budget=user_budget)
    # Print the plan
    print_maintenance_plan(plan)
