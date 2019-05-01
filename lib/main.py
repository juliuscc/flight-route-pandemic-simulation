from read import read_routes_from_file
from read_airports import read_airports_from_file
from betweenness import get_betweenness_value
import networkx as nx

routes = read_routes_from_file("../input/routes.dat")
airportDict = read_airports_from_file("../input/airports.dat") # Dictionary with {'id': (0 = airport name, 1 = city, 2 = country)}

G = nx.DiGraph()
G.add_edges_from(routes)

sorted_list = get_betweenness_value(G)

print(sorted_list[0])
