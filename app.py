import streamlit as st
import pandas as pd
import json
import folium
from streamlit_folium import st_folium

from dp_optimization.dp_scheduler import schedule_buses, schedule_metro_lines
from dp_optimization.dp_maintenance import allocate_maintenance
from shared.data_loader import load_data

from shortest_path.dijkstra import dijkstra
from shortest_path.dijkstra_traffic import dijkstra_with_traffic
from shortest_path.astar_emergency import astar

from mst import compute_hybrid_mst


# إعداد الصفحة
st.set_page_config(page_title="Smart City Transportation System", layout="wide")
st.title("🚦 Smart City Transportation Optimization")

# --- Load Data ---
neighborhoods = load_data("neighborhoods")
facilities = load_data("facilities")
locations = load_data("locations")
roads = load_data("roads")

# Convert to coordinate mapping
node_coords = {}
for _, row in neighborhoods.iterrows():
    node_coords[str(row["id"]) ] = (row["y_coordinate"], row["x_coordinate"])  # (lat, lon)
for _, row in facilities.iterrows():
    node_coords[row["id"]] = (row["y_coordinate"], row["x_coordinate"])

# --- Create Base Map ---
m = folium.Map(location=[30.05, 31.25], zoom_start=11)

# --- Add neighborhoods ---
for _, row in neighborhoods.iterrows():
    folium.Marker(
        location=[row["y_coordinate"], row["x_coordinate"]],
        popup=f"{row['name']} (Neighborhood)",
        icon=folium.Icon(color="blue", icon="home")
    ).add_to(m)

# --- Add facilities ---
facility_colors = {
    "EDUCATION": "orange",
    "MEDICAL": "red",
    "AIRPORT": "black",
    "TRANSIT_HUB": "cadetblue",
    "TOURISM": "purple",
    "SPORTS": "lightblue",
    "BUSINESS": "darkgreen",
    "COMMERCIAL": "lightgreen"
}

facility_icons = {
    "EDUCATION": "graduation-cap",
    "MEDICAL": "plus-sign",
    "AIRPORT": "plane",
    "TRANSIT_HUB": "road",
    "TOURISM": "info-sign",
    "SPORTS": "flag",
    "BUSINESS": "usd",
    "COMMERCIAL": "shopping-cart"
}

for _, row in facilities.iterrows():
    ftype = row["type"]
    color = facility_colors.get(ftype, "gray")
    icon = facility_icons.get(ftype, "info-sign")
    folium.Marker(
        location=[row["y_coordinate"], row["x_coordinate"]],
        popup=f"{row['name']} ({ftype})",
        icon=folium.Icon(color=color, icon=icon)
    ).add_to(m)

# Add roads as grey lines
for _, row in roads.iterrows():
    u, v = str(row["from_id"]), str(row["to_id"])
    if u in node_coords and v in node_coords:
        folium.PolyLine(locations=[node_coords[u], node_coords[v]], color="gray", weight=1).add_to(m)

# --- Sidebar Actions ---
st.sidebar.header("Choose your action")
action = st.sidebar.selectbox("What would you like to do?", [
    "Suggest new road network",
    "Find best route between two locations",
    "Simulate emergency response",
    "Visualize public transport scheduling",
    "Reduce traffic congestion at intersections",
    "Plan road maintenance"
])

display_mode = st.sidebar.radio("Display Mode", ["Table", "Text"])

# Initialize session state for maintenance plan
if "maintenance_plan" not in st.session_state:
    st.session_state.maintenance_plan = []

# --- 1. Suggest new road network ---
if action == "Suggest new road network":
    st.subheader("🛣️ Optimized Road Network (MST)")

    # 🔘 خيارات التكلفة حسب الأولوية
    st.markdown("### 🔧 Cost Adjustment Settings:")
    use_custom_cost = st.checkbox("Apply priority-based cost reduction", value=True)
    pop_factor = st.slider("Population factor (0.5 = 50%)", 0.5, 1.0, 0.8, step=0.05)
    fac_factor = st.slider("Facility factor (0.5 = 50%)", 0.5, 1.0, 0.7, step=0.05)

    # 🔘 تحديد الميزانية
    st.markdown("### 💰 Budget Constraint (Optional):")
    limit_toggle = st.checkbox("Limit new roads cost to a maximum budget")
    if limit_toggle:
        budget_value = st.number_input("Set max budget for new roads (in Million EGP):", min_value=0.0, value=8000.0, step=100.0)
    else:
        budget_value = 9999999  # قيمة ضخمة لو الميزانية مش مفعّلة

    # زرار الحساب
    if st.button("Generate Road Network"):
        st.session_state["mst_result"] = compute_hybrid_mst(
            apply_priority=use_custom_cost,
            population_factor=pop_factor,
            facility_factor=fac_factor,
            limit_budget=limit_toggle,
            max_budget=budget_value
        )

        # عرض النتائج
    if "mst_result" in st.session_state:
        final_mst, total_cost, num_existing = st.session_state["mst_result"]

        st.success(f"💰 Total cost for new roads: {total_cost:.2f}M EGP")
        st.info(f"➕ Existing roads added to complete connectivity: {num_existing}")

        for cost, u, v, is_new in final_mst:
            if u in node_coords and v in node_coords:
                color = "green" if is_new else "gray"
                tooltip = f"{u} ↔ {v} | Cost: {cost:.2f}M EGP | Type: {'NEW' if is_new else 'EXISTING'}"
                folium.PolyLine(
                    locations=[node_coords[u], node_coords[v]],
                    color=color,
                    weight=4,
                    tooltip=tooltip
                ).add_to(m)

        # رسم الطرق على الخريطة
        for cost, u, v, is_new in final_mst:
            if u in node_coords and v in node_coords:
                color = "green" if is_new else "yellow"
                tooltip = f"{u} ↔ {v} | Cost: {cost:.2f}M EGP | Type: {'NEW' if is_new else 'EXISTING'}"
                folium.PolyLine(
                    locations=[node_coords[u], node_coords[v]],
                    color=color,
                    weight=4,
                    tooltip=tooltip
                ).add_to(m)

    

# --- 2. Best route ---
elif action == "Find best route between two locations":
    algo_choice = st.radio("Choose algorithm", ["Dijkstra", "Dijkstra with Traffic"])
    start = st.selectbox("Start Location", locations["name"])
    end = st.selectbox("Destination Location", locations["name"])

    name_to_id = {str(row["name"]).strip().lower(): str(row["id"]) for _, row in locations.iterrows()}
    id_to_name = {str(row["id"]): str(row["name"]).strip() for _, row in locations.iterrows()}

    graph = {}
    for _, row in roads.iterrows():
        f, t, d = row["from_id"], row["to_id"], row["distance_km"]
        graph.setdefault(f, []).append((t, d))
        graph.setdefault(t, []).append((f, d))

    start_id = name_to_id[start.strip().lower()]
    end_id = name_to_id[end.strip().lower()]

    # ⬅️ نخلي اختيار الفترة يظهر دايمًا لما يختار الخوارزمية دي
    if algo_choice == "Dijkstra with Traffic":
        period = st.selectbox("Select traffic period", ["morning", "afternoon", "evening", "night"])
    else:
        period = None

    if st.button("Calculate Best Route"):
        if algo_choice == "Dijkstra":
            path, cost = dijkstra(graph, start_id, end_id)
        else:
            traffic = load_data("traffic")
            traffic_data = {
                row["roadid"]: {
                    "morning": row["morning_peakveh/h"],
                    "afternoon": row["afternoonveh/h"],
                    "evening": row["evening_peakveh/h"],
                    "night": row["nightveh/h"]
                }
                for _, row in traffic.iterrows()
            }
            path, cost = dijkstra_with_traffic(graph, traffic_data, start_id, end_id, period)

        st.session_state["best_path"] = path
        st.session_state["best_cost"] = cost

    if "best_path" in st.session_state and st.session_state["best_path"]:
        path = st.session_state["best_path"]
        cost = st.session_state["best_cost"]
        path_names = [id_to_name.get(p, p) for p in path]
        st.success(f"Total Distance: {cost:.2f} km")
        for step in path_names:
            st.markdown(f"- {step}")
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            if u in node_coords and v in node_coords:
                folium.PolyLine([node_coords[u], node_coords[v]], color="green", weight=4).add_to(m)


# --- 3. Emergency response ---
elif action == "Simulate emergency response":
    st.subheader("🚑 Emergency Routing Simulation")
    start = st.selectbox("Your Location", locations["name"])
    period = st.selectbox("Select time period for emergency simulation", ["Morning", "Afternoon", "Evening", "Night"])

    # تحويل الأسماء إلى ID والعكس
    name_to_id = {str(row["name"]).strip().lower(): str(row["id"]) for _, row in locations.iterrows()}
    id_to_name = {str(row["id"]): str(row["name"]).strip() for _, row in locations.iterrows()}
    coords = {str(row["id"]): (row["y"], row["x"]) for _, row in locations.iterrows()}

    graph = {}
    for _, row in roads.iterrows():
        f, t, d = row["from_id"], row["to_id"], row["distance_km"]
        graph.setdefault(f, []).append((t, d))
        graph.setdefault(t, []).append((f, d))

    start_id = name_to_id[start.strip().lower()]
    hospitals = locations[locations["type"].str.contains("medical", case=False)]["id"].astype(str).tolist()

    if st.button("Simulate Emergency Route"):
        best_path = []
        best_distance = float("inf")
        nearest = None

        for hid in hospitals:
            path, dist = astar(graph, coords, start_id, hid)
            if path and dist < best_distance:
                best_path = path
                best_distance = dist
                nearest = hid

        # خزن البيانات في session_state
        st.session_state["emergency_path"] = best_path
        st.session_state["emergency_distance"] = best_distance
        st.session_state["emergency_hospital"] = nearest

        # 🔄 تحديث emergency_routes.json فعليًا
        emergency_edges = []
        for i in range(len(best_path) - 1):
            edge = {
                "from_id": best_path[i],
                "to_id": best_path[i + 1],
                "period": period
            }
            emergency_edges.append(edge)

        with open("shared/emergency_routes.json", "w") as f:
            json.dump(emergency_edges, f, indent=4)

    # عرض النتائج لو متخزنة
    if "emergency_path" in st.session_state and st.session_state["emergency_path"]:
        path = st.session_state["emergency_path"]
        distance = st.session_state["emergency_distance"]
        nearest = st.session_state["emergency_hospital"]

        st.success(f"🏥 Nearest hospital: {id_to_name[nearest]}")
        for step in path:
            st.markdown(f"- {id_to_name.get(step, step)}")
        st.info(f"🛣️ Total Distance: {distance:.2f} km")

        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            if u in node_coords and v in node_coords:
                folium.PolyLine(
                    locations=[node_coords[u], node_coords[v]],
                    color="red", weight=5,
                    tooltip=f"{id_to_name.get(u)} → {id_to_name.get(v)}"
                ).add_to(m)

# --- 4. Public Transport Scheduling ---
elif action == "Visualize public transport scheduling":
    st.subheader("🚌 Optimized Transit Scheduling")
    total_buses = st.number_input("Enter total available buses:", min_value=1, value=60)
    total_trains = st.number_input("Enter total available metro trains:", min_value=1, value=20)

    # Initialize session_state if not exists
    if "bus_plan" not in st.session_state:
        st.session_state.bus_plan = {}
    if "metro_plan" not in st.session_state:
        st.session_state.metro_plan = {}

    if st.button("Generate Transit Schedules"):
        st.session_state.bus_plan = schedule_buses(total_buses)
        st.session_state.metro_plan = schedule_metro_lines(total_trains)

    bus_plan = st.session_state.bus_plan
    metro_plan = st.session_state.metro_plan

    # Load full route data
    bus_routes = load_data("bus_routes")
    metro_lines = load_data("metro_lines")

    if bus_plan or metro_plan:
        if display_mode == "Table":
            st.subheader("🚌 Bus Allocation")
            st.dataframe(pd.DataFrame(list(bus_plan.items()), columns=["RouteID", "Assigned Buses"]))
            st.subheader("🚇 Metro Allocation")
            st.dataframe(pd.DataFrame(list(metro_plan.items()), columns=["LineID", "Assigned Trains"]))
        else:
            st.subheader("🚌 Bus Allocation")
            for route, count in bus_plan.items():
                st.write(f"Route {route}: {count} buses")
            st.subheader("🚇 Metro Allocation")
            for line, count in metro_plan.items():
                st.write(f"Line {line}: {count} trains")

        # Draw bus routes
        for _, row in bus_routes.iterrows():
            route_id = row["routeid"]
            if bus_plan.get(route_id, 0) > 0:
                stops = row["stopscomma_separated_ids"].split(",")
                coords = [node_coords[s] for s in stops if s in node_coords]
                if len(coords) >= 2:
                    folium.PolyLine(
                        locations=coords,
                        color="blue",
                        weight=3,
                        tooltip=f"🚌 Route {route_id}: {bus_plan[route_id]} buses"
                    ).add_to(m)

        # Draw metro lines
        for _, row in metro_lines.iterrows():
            line_id = row["lineid"]
            if metro_plan.get(line_id, 0) > 0:
                stations = row["stationscomma_separated_ids"].split(",")
                coords = [node_coords[s] for s in stations if s in node_coords]
                if len(coords) >= 2:
                    folium.PolyLine(
                        locations=coords,
                        color="purple",
                        weight=3,
                        tooltip=f"🚇 Line {line_id}: {metro_plan[line_id]} trains"
                    ).add_to(m)


# --- 5. Traffic Signal Optimization ---
elif action == "Reduce traffic congestion at intersections":
    st.subheader("🚦 Smart Traffic Signal Timing")
    st.info("🚧 This will apply greedy logic to reduce congestion at key intersections.")

    if st.button("Run Greedy Signal Optimization"):
        result_df = pd.read_csv("greedy_signal_results.csv")
        st.session_state.greedy_results = result_df

    if "greedy_results" in st.session_state:
        result_df = st.session_state.greedy_results
        st.dataframe(result_df)

        # Visualize intersections on the map
        direction_colors = {
            'north': 'blue',
            'south': 'green',
            'east': 'orange',
            'west': 'purple',
            'unknown': 'gray'
        }
        period = st.selectbox("Select time period to visualize:", [
            "morning_peakveh/h_green_light",
            "afternoonveh/h_green_light",
            "evening_peakveh/h_green_light",
            "nightveh/h_green_light"
        ])

        for _, row in result_df.iterrows():
            node = row['intersection_id']
            if node in node_coords:
                dir_value = row.get(period, "unknown")
                folium.CircleMarker(
                    location=node_coords[node],
                    radius=8,
                    color=direction_colors.get(dir_value, "gray"),
                    fill=True,
                    fill_opacity=0.8,
                    tooltip=f"Intersection {node} → {dir_value.title()}"
                ).add_to(m)

# --- 6. Maintenance Planning ---
elif action == "Plan road maintenance":
    st.subheader("🚧 Road Maintenance Planning")
    budget = st.number_input(
        "Enter your available maintenance budget (in million EGP):",
        min_value=0.0,
        value=15.0,
        step=0.5
    )

    if st.button("Generate Maintenance Plan"):
        st.session_state.maintenance_plan = allocate_maintenance(budget=budget)

    plan = st.session_state.maintenance_plan

    if plan:
        if display_mode == "Table":
            df = pd.DataFrame(plan)
            st.dataframe(df[["FromID", "ToID", "Condition", "MaintenanceCost"]])
        else:
            for r in plan:
                st.write(f"🛣️ {r['FromID']} → {r['ToID']} | Condition: {r['Condition']} | Cost: {r['MaintenanceCost']:.2f}M EGP")

        total = sum(r["MaintenanceCost"] for r in plan)
        st.success(f"Total Cost of Selected Roads: {total:.2f}M EGP")

        for r in plan:
            u, v = str(r["FromID"]), str(r["ToID"])
            if u in node_coords and v in node_coords:
                folium.PolyLine(
                    locations=[node_coords[u], node_coords[v]],
                    color="red", weight=4,
                    tooltip=f"🛠️ Condition: {r['Condition']} | Cost: {r['MaintenanceCost']:.2f}M"
                ).add_to(m)

# --- Show Unified Map ---
st.subheader("🗺️ Cairo Map Overview")
st_folium(m, height=550, width="100%")

st.markdown("---")
st.caption("Runtime Terror | CSE112 - Design and Analysis of Algorithms Project")
st.caption("Team Member 1: Omnia Adel Saber")
st.caption("Team Member 2: Mariam Elrafei Mohamed")
st.caption("Team Member 3: Abdelrahman Amr Mohamed")
st.caption("Team Member 4: Shams Abd Elhalim Abo Ghannam")
