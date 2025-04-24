
import streamlit as st
import pandas as pd
from dp_optimization.dp_scheduler import schedule_buses, schedule_metro_lines
from dp_optimization.dp_maintenance import allocate_maintenance

# إعداد الصفحة
st.set_page_config(page_title="Smart City Transportation System", layout="wide")
st.title("🚦 Smart City Transportation Optimization")

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

# --- 1. Suggest new road network ---
if action == "Suggest new road network":
    st.subheader("🛣️ Optimized Road Network (MST)")
    st.info("🚧 This feature will generate a Minimum Spanning Tree network once implemented.")

# --- 2. Best route ---
elif action == "Find best route between two locations":
    st.subheader("🧭 Find the Shortest Route")
    st.info("🚧 This feature will calculate shortest route using Dijkstra or A* once added.")

# --- 3. Emergency response ---
elif action == "Simulate emergency response":
    st.subheader("🚑 Emergency Routing Simulation")
    st.info("🚧 This will simulate emergency vehicle routing to the nearest hospital.")

# --- 4. Public Transport Scheduling ---
elif action == "Visualize public transport scheduling":
    st.subheader("🚌 Optimized Transit Scheduling")
    total_buses = st.number_input("Enter total available buses:", min_value=1, value=60)
    total_trains = st.number_input("Enter total available metro trains:", min_value=1, value=20)

    if st.button("Generate Transit Schedules"):
        bus_plan = schedule_buses(total_buses)
        metro_plan = schedule_metro_lines(total_trains)

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

# --- 5. Traffic Signal Optimization ---
elif action == "Reduce traffic congestion at intersections":
    st.subheader("🚦 Smart Traffic Signal Timing")
    st.info("🚧 This will apply greedy logic to reduce congestion at key intersections.")

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
        plan = allocate_maintenance(budget=budget)

        if display_mode == "Table":
            df = pd.DataFrame(plan)
            st.dataframe(df[["FromID", "ToID", "Condition", "MaintenanceCost"]])
        else:
            for r in plan:
                st.write(f"🛣️ {r['FromID']} → {r['ToID']} | Condition: {r['Condition']} | Cost: {r['MaintenanceCost']:.2f}M EGP")

        total = sum(r["MaintenanceCost"] for r in plan)
        st.success(f"Total Cost of Selected Roads: {total:.2f}M EGP")

st.markdown("---")
st.caption("Runtime Terror | CSE112 - Design and Analysis of Algorithms Project")
