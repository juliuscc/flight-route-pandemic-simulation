import os
import networkx as nx
from flow_of_passengers import read_graph_with_importance
# from betweenness import get_betweenness_value
from simulation.driver import test_all_nodes, test_for_ranges
from statistics import mean

G = read_graph_with_importance()


def runForAllNodes():
    steps_for_all_nodes = test_all_nodes(G)
    print(steps_for_all_nodes)
    # Mean was 13.314068441064638 (but all over 20 were removed)
    print(f"Mean steps for all nodes: {mean(steps_for_all_nodes)}")


def runForRanges():
    steps_for_nodes = test_for_ranges(G)
    print(steps_for_nodes)


runForRanges()

# print(nx.average_clustering(G))
# sorted_list = get_betweenness_value(G)
# print(sorted_list[0])
