def prepare_graph(graph):

    for node in list(graph.nodes):
        attributes = graph.nodes.data()[node]
        graph.add_node(node, contaminated=False,
                       contaminated_step=-1, **attributes)

    return graph
