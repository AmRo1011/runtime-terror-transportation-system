import os
import sys

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph.graph_builder import Graph
from simulation.traffic_simulation import simulate_traffic, apply_traffic_penalty

def test_traffic():
    # Create a graph
    g = Graph()
    
    # Add edges
    g.add_edge('A', 'B', 5)
    g.add_edge('B', 'C', 3)
    g.add_edge('A', 'C', 7)
    
    # Simulate traffic
    print("\n=== Traffic Simulation Test ===")
    print("\n1. Initial Graph State:")
    print("Nodes:", g.get_nodes())
    print("Edges:", g.get_edges())
    
    # Simulate traffic
    simulate_traffic(g)
    print("\n2. After Traffic Simulation:")
    print("Edges with traffic levels:", g.get_edges())
    
    # Apply traffic penalty
    apply_traffic_penalty(g)
    print("\n3. After Applying Traffic Penalty:")
    print("Edges with adjusted weights:", g.get_edges())
    print("\n=== Test Completed ===")

if __name__ == "__main__":
    test_traffic()