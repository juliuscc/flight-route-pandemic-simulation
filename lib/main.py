import os
import errno
import networkx as nx
# from betweenness import get_betweenness_value
from statistics import mean

from flow_of_passengers import read_graph_with_importance
from flow_of_passengers import read_graph_w_extrapolated_flow

import simulation.driver as simDriver
import simulation.prepare_graph as prepare_graph

import eigen_vector_centrality
import betweenness


def runForRanges():
    G = read_graph_w_extrapolated_flow()

    print("Adding blocked nodes")
    exclude_eigen = eigen_vector_centrality.get_exclude_set(G, 20)
    exclude_betweenness = betweenness.get_betweenness_exclude_set(G, 20)

    prepare_graph.add_blocked_nodes(G, exclude_eigen)

    print("Creating additional data")
    prepare_graph.add_seir_states(G)

    folder = "results/sim"
    if not os.path.exists(folder):
        try:
            os.makedirs(folder, 0o700)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    ranges = simDriver.test_for_ranges(G)

    for rI, startRange in enumerate(ranges):
        for nI, startNode in enumerate(startRange):
            with open(f"{folder}/r{rI}-n{nI}.dat", "w") as f:
                for index, item in enumerate(startNode):
                    f.write(f"{index} {str(item)} \n")


runForRanges()

# print(nx.average_clustering(G))
# sorted_list = get_betweenness_value(G)
# print(sorted_list[0])
