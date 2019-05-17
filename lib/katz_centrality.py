import math
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def get_exclude_set(graph, elements):
    print("Calculating katz centrality")
    phi = (1 + math.sqrt(5)) / 2.0
    centrality_initial = nx.katz_centrality(graph, 1/phi - 0.01)

    centrality = [(c, v) for v, c in centrality_initial.items()]

    # Find the threashold that can be used to filter nodes.
    topElements = sorted(centrality, reverse=True)[:elements]
    minimum = min(topElements)
    maximum = max(topElements)

    topElements = [v for c, v in topElements]

    print(
        f"Using {elements} nodes with katz centrality in range [{minimum}:{maximum}]")
    print(topElements)
    return set(topElements)
