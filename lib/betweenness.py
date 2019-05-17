import networkx as nx


def get_betweenness_exclude_set(graph, elements):

    print("Calculating betweenness centrality")
    betweenness_nodes = nx.betweenness_centrality(graph, 100)

    centrality = [(c, v) for v, c in betweenness_nodes.items()]

    # Find the threashold that can be used to filter nodes.
    topElements = sorted(centrality, reverse=True)[:elements]
    minimum = min(topElements)
    maximum = max(topElements)

    topElements = [v for c, v in topElements]

    print(
        f"Using {elements} nodes with betweenness centrality in range [{minimum}:{maximum}]")
    print(topElements)
    return set(topElements)
