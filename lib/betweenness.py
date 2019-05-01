import networkx as nx


def get_betweenness_value(graph):

    betweenness_nodes = nx.betweenness_centrality(graph, 100)

    nodes = list()

    for key, value in betweenness_nodes.items():
        nodes.append((key, value))

    def get_betweenness_value(node):
        return node[1]

    sorted_list = sorted(nodes, key=get_betweenness_value)

    return sorted_list
