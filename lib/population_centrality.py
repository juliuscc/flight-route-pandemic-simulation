import math
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def get_exclude_set(graph, elements):
    print("Calculating centrality based on population")

    centrality = [(graph.nodes[node_id]['population'], node_id)
                  for node_id in graph.nodes]

    # Find the threashold that can be used to filter nodes.
    topElements = sorted(centrality, reverse=True)[:elements]
    minimum = min(topElements)
    maximum = max(topElements)

    topElements = [v for c, v in topElements]

    print(
        f"Using {elements} nodes with population centrality in range [{minimum}:{maximum}]")
    print(topElements)
    return set(topElements)
