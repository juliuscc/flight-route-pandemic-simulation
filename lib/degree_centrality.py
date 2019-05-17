import math
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def get_exclude_set(graph, elements):
    print("Calculating degree centrality")
    centrality_initial = nx.degree_centrality(graph)

    centrality = [(c, v) for v, c in centrality_initial.items()]

    # Find the threashold that can be used to filter nodes.
    topElements = sorted(centrality, reverse=True)[:elements]
    minimum = min(topElements)
    maximum = max(topElements)

    topElements = [v for c, v in topElements]

    print(
        f"Using {elements} nodes with degree centrality in range [{minimum}:{maximum}]")
    print(topElements)
    return set(topElements)
