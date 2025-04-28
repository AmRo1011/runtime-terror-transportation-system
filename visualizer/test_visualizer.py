from graph.graph_builder import Graph
from visualizer import draw_graph

def test_visualizer():
    # Create a graph
    g = Graph()
    
    # Add edges
    g.add_edge('A', 'B', 5)
    g.add_edge('B', 'C', 3)
    g.add_edge('A', 'C', 7)
    g.add_edge('B', 'D', 4)
    g.add_edge('C', 'D', 2)
    
    # Draw the graph
    draw_graph(g, title="Test Graph")

if __name__ == "__main__":
    test_visualizer() 