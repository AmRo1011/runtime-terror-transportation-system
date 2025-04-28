import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_graph():
    try:
        print("\n=== Testing Graph Module ===")
        from graph.graph_builder import Graph
        g = Graph()
        g.add_edge('A', 'B', 5)
        g.add_edge('B', 'C', 3)
        g.add_edge('A', 'C', 7)
        print("Nodes:", g.get_nodes())
        print("Edges:", g.get_edges())
        return g
    except Exception as e:
        print(f"Error in Graph module: {e}")
        return None

def test_mst(graph):
    try:
        print("\n=== Testing MST Module ===")
        from mst.mst import kruskal_mst
        mst = kruskal_mst(graph)
        print("Minimum Spanning Tree:", mst)
        return mst
    except Exception as e:
        print(f"Error in MST module: {e}")
        return None

def test_traffic(graph):
    try:
        print("\n=== Testing Traffic Simulation Module ===")
        from simulation.traffic_simulation import simulate_traffic, apply_traffic_penalty
        
        print("Before traffic simulation:")
        print("Edges:", graph.get_edges())
        
        simulate_traffic(graph)
        print("\nAfter traffic simulation:")
        print("Edges:", graph.get_edges())
        
        apply_traffic_penalty(graph)
        print("\nAfter applying traffic penalty:")
        print("Edges:", graph.get_edges())
    except Exception as e:
        print(f"Error in Traffic Simulation module: {e}")

def test_visualizer(graph):
    try:
        print("\n=== Testing Visualizer Module ===")
        from visualizer.visualizer import draw_graph
        print("Drawing graph... (This will open a matplotlib window)")
        draw_graph(graph, title="Test Graph")
    except Exception as e:
        print(f"Error in Visualizer module: {e}")

if __name__ == "__main__":
    print("Starting comprehensive test of all modules...")
    
    # Test Graph module
    graph = test_graph()
    if graph is None:
        print("Graph test failed. Cannot proceed with other tests.")
        sys.exit(1)
    
    # Test MST module
    mst = test_mst(graph)
    if mst is None:
        print("MST test failed. Proceeding with remaining tests...")
    
    # Test Traffic Simulation module
    test_traffic(graph)
    
    # Test Visualizer module
    test_visualizer(graph)
    
    print("\n=== All tests completed ===") 