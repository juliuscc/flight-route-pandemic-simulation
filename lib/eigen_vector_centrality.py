import math
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def get_exclude_set(graph, elements):
    eigencentrality = nx.eigenvector_centrality(graph)
    centrality = [(c, v) for v, c in eigencentrality.items()]

    # Find the threashold that can be used to filter nodes.
    topElements = sorted(centrality, reverse=True)[:elements]

    topElements = [v for c, v in centrality]

    minimum = min(topElements)
    maximum = max(topElements)

    print(
        f"Using {elements} nodes with eigenvector centrality in range [{minimum}:{maximum}]")

    return set(topElements)
