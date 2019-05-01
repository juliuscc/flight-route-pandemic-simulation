import networkx as nx


def iterate_graph(graph, step):

    def is_contaminated(node):
        return node[1]['contaminated']

    def get_node_id(node):
        return node[0]

    contaminated_nodes = set(
        map(get_node_id, filter(is_contaminated, graph.nodes.data())))

    neighbours_with_doublet = list(map(
        lambda node: list(graph.adj[node]),
        contaminated_nodes
    ))

    def flatten(l): return [item for sublist in l for item in sublist]

    neighbours = set(flatten(neighbours_with_doublet))

    for neighbour in neighbours:
        if(not is_contaminated(list(graph.nodes.data())[neighbour])):
            graph.add_node(
                neighbour,
                contaminated=True,
                contaminated_step=step
            )
