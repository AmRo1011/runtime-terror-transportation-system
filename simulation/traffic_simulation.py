# traffic_simulation.py

import random

def simulate_traffic(graph, max_traffic_level=10):
    """
    Randomly assign traffic levels to edges to simulate different scenarios.
    """
    new_edges = []
    for weight, u, v, _ in graph.get_edges():
        traffic_level = random.randint(0, max_traffic_level)
        new_edges.append((weight, u, v, traffic_level))
    graph.edges = new_edges

def apply_traffic_penalty(graph):
    """
    Increase edge weights according to traffic level.
    """
    new_edges = []
    for weight, u, v, traffic_level in graph.get_edges():
        penalty = traffic_level * 0.1  # Increase 10% per traffic level
        new_weight = weight * (1 + penalty)
        new_edges.append((new_weight, u, v, traffic_level))
    graph.edges = new_edges