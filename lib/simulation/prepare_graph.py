
def add_seir_states(graph):
    """Take a graph with population state and add SEIR states to it 
        for use in calculations"""
    for node in graph.nodes:
        # We assume that population has already been defined here
        sumNeighbourWeights = sum([
            graph.nodes[nId]['population']
            for nId in graph.adj[node]
        ])

        graph.nodes[node].susceptible = graph.nodes[node]['population']
        graph.nodes[node].exposed = 0
        graph.nodes[node].infectious = 0
        graph.nodes[node].recovered = 0
        graph.nodes[node].sum_neighbour_weights = sumNeighbourWeights

    return graph
