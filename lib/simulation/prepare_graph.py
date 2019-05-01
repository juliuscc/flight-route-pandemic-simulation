def prepare_graph(graph):

    for node in list(graph.nodes):
        graph.add_node(node, contaminated=False)

    return graph
