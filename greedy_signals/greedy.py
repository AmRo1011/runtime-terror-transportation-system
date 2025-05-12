import pandas as pd
import json
from shared.data_loader import load_data

def load_emergency_routes(file_path="emergency_routes.json"):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def main():
    traffic = load_data("traffic")
    roads = load_data("roads")
    locations = load_data("locations")

    # Extract coordinates for direction estimation
    coords = {str(row['id']): (row['x'], row['y']) for _, row in locations.iterrows()}

    # Load emergency routes
    emergency_routes = load_emergency_routes()
    emergency_set = {(e['from_id'], e['to_id'], e['period']) for e in emergency_routes}

    traffic[['From', 'To']] = traffic['roadid'].str.split('-', expand=True)

    def estimate_direction(from_id, to_id):
        if from_id not in coords or to_id not in coords:
            return "unknown"
        x1, y1 = coords[from_id]
        x2, y2 = coords[to_id]
        dx, dy = x2 - x1, y2 - y1
        if abs(dx) > abs(dy):
            return 'east' if dx > 0 else 'west'
        else:
            return 'north' if dy > 0 else 'south'

    results = []
    periods = ['morning_peakveh/h', 'afternoonveh/h', 'evening_peakveh/h', 'nightveh/h']

    # ✅ Period mapping for emergency JSON
    period_map = {
        'morning_peakveh/h': 'Morning',
        'afternoonveh/h': 'Afternoon',
        'evening_peakveh/h': 'Evening',
        'nightveh/h': 'Night'
    }

    for to_node in traffic['To'].unique():
        intersect_traffic = traffic[traffic['To'] == to_node]
        entry_directions = {p: {} for p in periods}

        for _, row in intersect_traffic.iterrows():
            from_id, to_id = row['From'], row['To']
            direction = estimate_direction(from_id, to_id)
            for p in periods:
                entry_directions[p][direction] = entry_directions[p].get(direction, 0) + row[p]

        result = {"intersection_id": to_node}
        for p in periods:
            period_name = period_map[p]
            emg_match = [estimate_direction(f, t) for f, t, per in emergency_set if t == to_node and per == period_name]
            if emg_match:
                result[f"{p}_green_light"] = emg_match[0]  # emergency direction
            else:
                # Apply greedy: direction with max traffic
                if entry_directions[p]:
                    result[f"{p}_green_light"] = max(entry_directions[p], key=entry_directions[p].get)
                else:
                    result[f"{p}_green_light"] = "unknown"

        results.append(result)

    pd.DataFrame(results).to_csv("greedy_signal_results.csv", index=False)
    print("✅ Greedy Signal Timing Done. Check greedy_signal_results.csv")

if __name__ == "__main__":
    main()
