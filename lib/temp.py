import networkx as nx
from simulation.prepare_graph import prepare_graph

graph = nx.fast_gnp_random_graph(10, 0.2, None, True)

prepare_graph(graph)

# graph.nodes[0]['day'] = 'Monday'
# graph.nodes[1]['day'] = 'Tuesday'

# graph.add_node(0, day='Monday')

print(graph.nodes)
print(graph.nodes.data())
print(graph.edges)
print(graph.graph)
