# mst.py

class DisjointSet:
    def __init__(self, nodes):
        self.parent = {node: node for node in nodes}

    def find(self, node):
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            self.parent[root_v] = root_u

def kruskal_mst(graph):
    mst = []
    disjoint_set = DisjointSet(graph.get_nodes())
    sorted_edges = sorted(graph.get_edges(), key=lambda x: x[0])  # Sort by weight

    for weight, u, v, traffic_level in sorted_edges:
        if disjoint_set.find(u) != disjoint_set.find(v):
            disjoint_set.union(u, v)
            mst.append((u, v, weight))

    return mst