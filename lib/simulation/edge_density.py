import networkx as nx

def edge_density(graph):
    d = nx.density(graph)
    print("The edge density of the graph: ", d)
    return d

