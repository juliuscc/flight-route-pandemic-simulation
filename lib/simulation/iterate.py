import networkx as nx
import random


def infect_node(graph, node_id, step=0):
    attributes = graph.nodes.data()[node_id]
    attributes['contaminated'] = True
    attributes['contaminated_step'] = step

    graph.add_node(
        node_id,
        **attributes
    )


def iterate_graph(graph, step):

    # Get all infected nodes
    infected_nodes = filter(
        lambda node: node[1]['contaminated'],
        graph.nodes.data()
    )

    # Iterate over every infected node
    for infected in infected_nodes:
        infected_id = infected[0]
        infection_probability = infected[1]['importance']

        # Get all healthy neighbours of the infected node
        neighbours = graph.adj[infected_id]
        healthy_neighbours = [neighbour for neighbour in neighbours if not graph.nodes.data()[
            neighbour]['contaminated']]

        # Do a coin flip for every healthy neighbour and infect
        for neighbour in healthy_neighbours:
            if random.random() < infection_probability:
                infect_node(graph, neighbour)
