from graph.graph_builder import Graph
from mst import kruskal_mst

def test_mst():
    # Create a graph
    g = Graph()
    
    # Add edges
    g.add_edge('A', 'B', 5)
    g.add_edge('B', 'C', 3)
    g.add_edge('A', 'C', 7)
    g.add_edge('B', 'D', 4)
    g.add_edge('C', 'D', 2)
    
    # Get MST
    mst = kruskal_mst(g)
    print("Minimum Spanning Tree:", mst)

if __name__ == "__main__":
    test_mst() 