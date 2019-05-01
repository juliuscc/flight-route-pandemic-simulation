def prepare_graph(graph):

    for node in list(graph.nodes):
        graph.add_node(node, contaminated=False, contaminated_step=-1)

    return graph
