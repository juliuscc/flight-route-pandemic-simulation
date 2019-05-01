from read import read_routes_from_file
import networkx as nx

routes = read_routes_from_file("../input/routes.dat")

G = nx.DiGraph()

G.add_edges_from(routes)

print(routes[0])
print(G.number_of_nodes())
