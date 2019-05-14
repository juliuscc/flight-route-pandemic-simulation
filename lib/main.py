import os
import networkx as nx
# from betweenness import get_betweenness_value
from statistics import mean

from flow_of_passengers import read_graph_with_importance

import lib.simulation.driver as simDriver
import lib.simulation.prepare_graph as prepare_graph

G = read_graph_with_importance()
prepare_graph.add_seir_states(G)


def runForRanges():
    steps_for_nodes = simDriver.test_for_ranges(G)
    print(steps_for_nodes)


runForRanges()

# print(nx.average_clustering(G))
# sorted_list = get_betweenness_value(G)
# print(sorted_list[0])
