import networkx as nx
from simulation.prepare_graph import prepare_graph
from simulation.iterate import iterate_graph

graph = nx.fast_gnp_random_graph(5, 0.4, 1)

prepare_graph(graph)

graph.add_node(0, contaminated=True, contaminated_step=0)

print(graph.edges)
print(graph.nodes.data())

iterate_graph(graph, 1)
print(graph.nodes.data())

iterate_graph(graph, 2)
print(graph.nodes.data())

iterate_graph(graph, 3)
print(graph.nodes.data())
