# visualizer.py

import matplotlib.pyplot as plt
import networkx as nx

def draw_graph(graph, title="Graph"):
    G = nx.Graph()
    for weight, u, v, traffic_level in graph.get_edges():
        G.add_edge(u, v, weight=round(weight, 2))

    pos = nx.spring_layout(G, seed=42)
    edge_labels = nx.get_edge_attributes(G, 'weight')

    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1200, font_size=10, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title(title)
    plt.show()