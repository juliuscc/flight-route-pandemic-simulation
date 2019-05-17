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
import katz_centrality
import degree_centrality
import population_centrality


def runForRanges(G, block_set, prefix=""):

    if len(block_set) > 0:
        prepare_graph.add_blocked_nodes(G, block_set)

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
            with open(f"{folder}/{prefix}-r{rI}-n{nI}.dat", "w") as f:
                for index, item in enumerate(startNode):
                    f.write(f"{index} {str(item)} \n")


G = read_graph_w_extrapolated_flow()
empty = set()
# runForRanges(G, empty, "base")
# exclude_eigen = eigen_vector_centrality.get_exclude_set(G, 20)
# runForRanges(G, exclude_eigen, "eigen")
# exclude_betweenness = betweenness.get_betweenness_exclude_set(G, 20)
# runForRanges(G, exclude_betweenness, "betweenness")
exclude_population = population_centrality.get_exclude_set(G, 20)
runForRanges(G, exclude_population, "population")


# print(nx.average_clustering(G))
# sorted_list = get_betweenness_value(G)
# print(sorted_list[0])

# plot "sim/base-r0-n0.dat" u 1: 2 axes x1y1 w lines lw 2 title "Susceptible", "sim/base-r0-n0.dat" u 1: 3 axes x1y1 w lines lw 2 title "Exposed", "sim/base-r0-n0.dat" u 1: 4 axes x1y1 w lines lw 2 title "Infected", "sim/base-r0-n0.dat" u 1: 5 axes x1y1 w lines lw 2 title "Recovered"
# plot "sim/base-r0-n0.dat" u 1:4 axes x1y1 w lines lw 2 title "Infected", "sim/base-r0-n0.dat" u 1:5 axes x1y1 w lines lw 2 title "Recovered", "sim/eigen-r0-n0.dat" u 1:4 axes x1y1 w lines lw 2 title "Infected - eigen", "sim/eigen-r0-n0.dat" u 1:5 axes x1y1 w lines lw 2 title "Recovered - eigen", "sim/betweenness-r0-n0.dat" u 1:4 axes x1y1 w lines lw 2 title "Infected - betweenness", "sim/betweenness-r0-n0.dat" u 1:5 axes x1y1 w lines lw 2 title "Recovered - betweenness", "sim/degree-r0-n0.dat" u 1:4 axes x1y1 w lines lw 2 title "Infected - degree", "sim/degree-r0-n0.dat" u 1:5 axes x1y1 w lines lw 2 title "Recovered - degree"
# plot "sim/base-r0-n0.dat" u 1:4 axes x1y1 w lines lw 2 title "Infected", "sim/base-r0-n0.dat" u 1:5 axes x1y1 w lines lw 2 title "Recovered", "sim/eigen-r0-n0.dat" u 1:4 axes x1y1 w lines lw 2 title "Infected - eigen", "sim/eigen-r0-n0.dat" u 1:5 axes x1y1 w lines lw 2 title "Recovered - eigen", "sim/betweenness-r0-n0.dat" u 1:4 axes x1y1 w lines lw 2 title "Infected - betweenness", "sim/betweenness-r0-n0.dat" u 1:5 axes x1y1 w lines lw 2 title "Recovered - betweenness", "sim/population-r0-n0.dat" u 1:4 axes x1y1 w lines lw 2 title "Infected - population", "sim/population-r0-n0.dat" u 1:5 axes x1y1 w lines lw 2 title "Recovered - population"

# Base
# plot "sim/base-r0-n0.dat" u 1: 2 axes x1y1 w lines lw 2 title "Susceptible", "sim/base-r0-n0.dat" u 1: 3 axes x1y1 w lines lw 2 title "Exposed", "sim/base-r0-n0.dat" u 1: 4 axes x1y1 w lines lw 2 title "Infected", "sim/base-r0-n0.dat" u 1: 5 axes x1y1 w lines lw 2 title "Recovered"
# plot "sim/base-r0-n0.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C74931" title "Recovered Upper", "sim/base-r0-n1.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C74931" notitle, "sim/base-r0-n2.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C74931" notitle, "sim/base-r1-n0.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C7C661" title "Recovered Median", "sim/base-r1-n1.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C7C661" notitle, "sim/base-r1-n2.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C7C661" notitle, "sim/base-r2-n0.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#9ACC8E" title "Recovered Lower", "sim/base-r2-n1.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#9ACC8E" notitle, "sim/base-r2-n2.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#9ACC8E" notitle

# Eigenvector
# plot "sim/eigen-r0-n0.dat" u 1: 2 axes x1y1 w lines lw 2 title "Susceptible", "sim/eigen-r0-n0.dat" u 1: 3 axes x1y1 w lines lw 2 title "Exposed", "sim/eigen-r0-n0.dat" u 1: 4 axes x1y1 w lines lw 2 title "Infected", "sim/eigen-r0-n0.dat" u 1: 5 axes x1y1 w lines lw 2 title "Recovered"
# plot "sim/eigen-r0-n0.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C74931" title "Recovered Upper", "sim/eigen-r0-n1.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C74931" notitle, "sim/eigen-r0-n2.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C74931" notitle, "sim/eigen-r1-n0.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C7C661" title "Recovered Median", "sim/eigen-r1-n1.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C7C661" notitle, "sim/eigen-r1-n2.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C7C661" notitle, "sim/eigen-r2-n0.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#9ACC8E" title "Recovered Lower", "sim/eigen-r2-n1.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#9ACC8E" notitle, "sim/eigen-r2-n2.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#9ACC8E" notitle

# Betweenness
# plot "sim/betweenness-r0-n0.dat" u 1: 2 axes x1y1 w lines lw 2 title "Susceptible", "sim/betweenness-r0-n0.dat" u 1: 3 axes x1y1 w lines lw 2 title "Exposed", "sim/betweenness-r0-n0.dat" u 1: 4 axes x1y1 w lines lw 2 title "Infected", "sim/betweenness-r0-n0.dat" u 1: 5 axes x1y1 w lines lw 2 title "Recovered"
# plot "sim/betweenness-r0-n0.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C74931" title "Recovered Upper", "sim/betweenness-r0-n1.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C74931" notitle, "sim/betweenness-r0-n2.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C74931" notitle, "sim/betweenness-r1-n0.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C7C661" title "Recovered Median", "sim/betweenness-r1-n1.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C7C661" notitle, "sim/betweenness-r1-n2.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C7C661" notitle, "sim/betweenness-r2-n0.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#9ACC8E" title "Recovered Lower", "sim/betweenness-r2-n1.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#9ACC8E" notitle, "sim/betweenness-r2-n2.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#9ACC8E" notitle

# Population
# plot "sim/population-r0-n0.dat" u 1: 2 axes x1y1 w lines lw 2 title "Susceptible", "sim/population-r0-n0.dat" u 1: 3 axes x1y1 w lines lw 2 title "Exposed", "sim/population-r0-n0.dat" u 1: 4 axes x1y1 w lines lw 2 title "Infected", "sim/population-r0-n0.dat" u 1: 5 axes x1y1 w lines lw 2 title "Recovered"
# plot "sim/population-r0-n0.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C74931" title "Recovered Upper", "sim/population-r0-n1.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C74931" notitle, "sim/population-r0-n2.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C74931" notitle, "sim/population-r1-n0.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C7C661" title "Recovered Median", "sim/population-r1-n1.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C7C661" notitle, "sim/population-r1-n2.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C7C661" notitle, "sim/population-r2-n0.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#9ACC8E" title "Recovered Lower", "sim/population-r2-n1.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#9ACC8E" notitle, "sim/population-r2-n2.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#9ACC8E" notitle

# Comparing
# susceptible
# plot "sim/base-r0-n0.dat" u 1: 2 axes x1y1 w lines lw 2 lt rgb "#C74931" title "Base", "sim/eigen-r0-n0.dat" u 1: 2 axes x1y1 w lines lw 2 lt rgb "#C7C661" title "Eigenvector centrality", "sim/betweenness-r0-n0.dat" u 1: 2 axes x1y1 w lines lw 2 lt rgb "#9ACC8E" title "Betweenness centrality", "sim/population-r0-n0.dat" u 1: 2 axes x1y1 w lines lw 2 lt rgb "#3436BF" title "Population"

# exposed
# plot  "sim/base-r0-n0.dat" u 1: 3 axes x1y1 w lines lw 2 lt rgb "#C74931" title "Base", "sim/eigen-r0-n0.dat" u 1: 3 axes x1y1 w lines lw 2 lt rgb "#C7C661" title "Eigenvector centrality", "sim/betweenness-r0-n0.dat" u 1: 3 axes x1y1 w lines lw 2 lt rgb "#9ACC8E" title "Betweenness centrality", "sim/population-r0-n0.dat" u 1: 3 axes x1y1 w lines lw 2 lt rgb "#3436BF" title "Population"

# infected
# plot "sim/base-r0-n0.dat" u 1: 4 axes x1y1 w lines lw 2 lt rgb "#C74931" title "Base", "sim/eigen-r0-n0.dat" u 1: 4 axes x1y1 w lines lw 2 lt rgb "#C7C661" title "Eigenvector centrality", "sim/betweenness-r0-n0.dat" u 1: 4 axes x1y1 w lines lw 2 lt rgb "#9ACC8E" title "Betweenness centrality", "sim/population-r0-n0.dat" u 1: 4 axes x1y1 w lines lw 2 lt rgb "#3436BF" title "Population"

# population
# plot "sim/base-r0-n0.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C74931" title "Base", "sim/eigen-r0-n0.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C7C661" title "Eigenvector centrality", "sim/betweenness-r0-n0.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#9ACC8E" title "Betweenness centrality", "sim/population-r0-n0.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#3436BF" title "Population"

# plot "sim/population-r0-n0.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C74931" title "Recovered r0-n0","sim/population-r0-n1.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C74931" title "Recovered r0-n1","sim/population-r0-n2.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C74931" title "Recovered r0-n2","sim/population-r1-n0.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C7C661" title "Recovered r1-n0","sim/population-r1-n1.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C7C661" title "Recovered r1-n1","sim/population-r1-n2.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#C7C661" title "Recovered r1-n2","sim/population-r2-n0.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#9ACC8E" title "Recovered r2-n0","sim/population-r2-n1.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#9ACC8E" title "Recovered r2-n1","sim/population-r2-n2.dat" u 1: 5 axes x1y1 w lines lw 2 lt rgb "#9ACC8E" title "Recovered r2-n2"
