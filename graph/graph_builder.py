# graph_builder.py

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = []

    def add_edge(self, u, v, weight, traffic_level=0):
        self.nodes.add(u)
        self.nodes.add(v)
        self.edges.append((weight, u, v, traffic_level))

    def get_nodes(self):
        return list(self.nodes)

    def get_edges(self):
        return self.edges