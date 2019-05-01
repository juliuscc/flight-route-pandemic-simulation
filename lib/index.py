from read import read_routes_from_file
from betweenness import get_betweenness_value
import networkx as nx

routes = read_routes_from_file("../input/routes.dat")

print(routes)

G = nx.DiGraph()
G.add_edges_from(routes)

sorted_list = get_betweenness_value(G)

print(sorted_list)
