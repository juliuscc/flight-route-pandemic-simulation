
# Returns the percentage of nodes that are contaminated


def check_progress(graph):
    num_of_nodes = graph.number_of_nodes()

    def is_contaminated(node):
        return node[1]['contaminated']

    def get_node_id(node):
        return node[0]

    contaminated_nodes = set(
        map(get_node_id, filter(is_contaminated, graph.nodes.data())))

    num_of_contaminated = len(contaminated_nodes)

    percentage = num_of_contaminated/num_of_nodes
    return percentage
