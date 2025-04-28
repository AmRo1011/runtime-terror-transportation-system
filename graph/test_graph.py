from graph_builder import Graph

def test_graph():
    # Create a new graph
    g = Graph()
    
    # Add some edges
    g.add_edge('A', 'B', 5)
    g.add_edge('B', 'C', 3)
    g.add_edge('A', 'C', 7)
    
    # Test nodes
    print("Nodes:", g.get_nodes())
    
    # Test edges
    print("Edges:", g.get_edges())

if __name__ == "__main__":
    test_graph() 