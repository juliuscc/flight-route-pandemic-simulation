import os
import networkx as nx
from read import read_routes_from_file
from read_airports import read_airports_from_file
from betweenness import get_betweenness_value
from simulation.driver import test_all_nodes
from statistics import mean

dirname = os.path.dirname(__file__)

routes_filename = os.path.join(dirname, '../input/routes.dat')
airports_filename = os.path.join(dirname, '../input/airports.dat')

routes = read_routes_from_file(routes_filename)

# Dictionary with {'id': (0 = airport name, 1 = city, 2 = country)}
airportDict = read_airports_from_file(airports_filename)

G = nx.Graph()
G.add_edges_from(routes)

steps_for_all_nodes = test_all_nodes(G)
print(steps_for_all_nodes)
print(f"Mean steps for all nodes: {mean(steps_for_all_nodes)}")

# print(nx.average_clustering(G))

# sorted_list = get_betweenness_value(G)

# print(sorted_list[0])
