from shared.preprocessing import clean_csv

# mapping between type name and actual file path
DATA_PATHS = {
    "neighborhoods": "shared/data/Neighborhoods.csv",
    "facilities": "shared/data/Facilities.csv",
    "roads": "shared/data/Existing_Roads.csv",
    "new_roads": "shared/data/Potential_New_Roads.csv",
    "bus_routes": "shared/data/Current_Bus_Routes.csv",
    "metro_lines": "shared/data/Current_Metro_Lines.csv",
    "traffic": "shared/data/Traffic_Flow_Patterns.csv",
    "demand": "shared/data/Transportation_Demand.csv",
    "greedy_intersections": "shared/data/greedy_intersections.csv",
    "locations": "shared/data/locations.csv"
}

def load_data(data_type: str):
    """
    Load a specific cleaned CSV dataset based on its type keyword.
    
    Available types:
    - neighborhoods, facilities, roads, new_roads
    - bus_routes, metro_lines, traffic, demand
    """
    path = DATA_PATHS.get(data_type.lower())
    if path:
        return clean_csv(path)
    else:
        raise ValueError(f"Unknown data type: {data_type}")
