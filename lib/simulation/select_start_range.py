import random

# This is only for the debugging
import pandas as pd
import networkx as nx


def range(G, elements=10, selectRange=0.1, randomSeed=123456789):
    """Returns semi-random high, middle and low range from the graph based on degree. 
    Elements are selected randomly from the nodes that fall into the selection ranges
    [:range], [center-range/2:center+range/2] and [-range:]"""
    degreesOfNodes = sorted([(d, n) for n, d in G.degree()], reverse=True)

    nInRange = int(len(degreesOfNodes) * selectRange)
    center = int(len(degreesOfNodes) / 2)
    dist = int(nInRange / 2)

    # Create ranges containing all elements in each selection range
    lRange = degreesOfNodes[0:nInRange]
    mRange = degreesOfNodes[center - dist: center + dist]
    hRange = degreesOfNodes[-nInRange:]

    allRanges = [lRange, mRange, hRange]

    # Prune the ranges until we have the correct number of elements in each.
    random.seed(randomSeed)
    revRanges = list()
    for r in allRanges:
        while(len(r) > elements):
            r.pop(random.randint(0, len(r) - 1))
        revRanges.append([(n, d) for d, n in r])

    return (revRanges)


if __name__ == '__main__':
    data = pd.read_csv("input/routes.dat", header=-1)
    routes = pd.DataFrame(data, columns=[2, 4]).rename(
        columns={2: "From", 4: "To"})

    # Creating network graph

    tuples = [tuple(x) for x in routes.values]

    G = nx.Graph()
    G.add_edges_from(tuples)

    # print(G.nodes)

    print(range(G))
